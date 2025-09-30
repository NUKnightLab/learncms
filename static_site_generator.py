#!/usr/bin/env python3
"""
New Static Site Generator for learncms

This script crawls https://learn.knightlab.com/ and generates static HTML files
that are fully portable with no external dependencies on S3 or other off-site media.
"""

import os
import sys
import json
import time
import re
from pathlib import Path
import argparse
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


class StaticSiteGenerator:
    def __init__(self, base_url, output_dir, static_dir='static'):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.static_dir = Path(static_dir)

        self.crawled_urls = set()
        self.failed_urls = []
        self.off_site_dependencies = []
        self.media_files = set()
        self.missing_local_assets = []

    def fetch_url(self, url, timeout=30):
        """Fetch a URL and return the content"""
        try:
            print(f"Fetching: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            request = Request(url, headers=headers)

            with urlopen(request, timeout=timeout) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '').lower()
                    return response.read(), content_type
                else:
                    print(f"Warning: {url} returned status {response.status}")
                    return None, None

        except HTTPError as e:
            print(f"HTTP Error {e.code} for {url}: {e.reason}")
            self.failed_urls.append((url, f"HTTP {e.code}: {e.reason}"))
            return None, None
        except URLError as e:
            print(f"URL Error for {url}: {e.reason}")
            self.failed_urls.append((url, f"URL Error: {e.reason}"))
            return None, None
        except Exception as e:
            print(f"Unexpected error for {url}: {e}")
            self.failed_urls.append((url, f"Error: {e}"))
            return None, None

    def get_lessons_from_api(self):
        """Get all lesson slugs from the JSON API"""
        lessons_url = f"{self.base_url}/lesson.json"
        content, _ = self.fetch_url(lessons_url)
        if content:
            try:
                lessons_data = json.loads(content.decode('utf-8'))
                return [data["slug"] for title, data in lessons_data.items()
                       if data.get("status") == "published"]
            except json.JSONDecodeError as e:
                print(f"Error parsing lessons JSON: {e}")
        return []

    def validate_media_dependencies(self, html_content, page_url):
        """
        Validate that all media dependencies are on-site.
        Fail loudly if any off-site dependencies are found.
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tags and attributes that can reference media
        media_tags = {
            'img': ['src', 'data-src'],
            'script': ['src'],
            'link': ['href'],
            'source': ['src'],
            'video': ['src', 'poster'],
            'audio': ['src'],
            'object': ['data'],
            'embed': ['src'],
            'iframe': ['src']
        }

        for tag_name, attrs in media_tags.items():
            for tag in soup.find_all(tag_name):
                for attr in attrs:
                    url = tag.get(attr)
                    if url:
                        self._check_media_url(url, page_url)

    def _check_media_url(self, url, page_url):
        """Check if a media URL is on-site or off-site"""
        if not url or url.startswith('#') or url.startswith('javascript:') or url.startswith('mailto:'):
            return

        # Handle protocol-relative URLs
        if url.startswith('//'):
            url = 'https:' + url

        # Handle relative URLs
        if not url.startswith(('http://', 'https://')):
            url = urljoin(page_url, url)

        parsed_url = urlparse(url)

        # Check if this is an off-site dependency
        if parsed_url.netloc and parsed_url.netloc != self.domain:
            # Special handling for media.knightlab.com - should be served locally
            if parsed_url.netloc == 'media.knightlab.com':
                return self._check_knightlab_media(url, parsed_url.path, page_url)

            # Allow certain CDNs that are acceptable
            allowed_cdns = [
                'cdn.knightlab.com',
                'fonts.googleapis.com',
                'fonts.gstatic.com',
                'ajax.googleapis.com',
                'code.jquery.com',
                'maxcdn.bootstrapcdn.com',
                'cdnjs.cloudflare.com',
                'www.googletagmanager.com'  # Allow Google Tag Manager
            ]

            if not any(cdn in parsed_url.netloc for cdn in allowed_cdns):
                dependency = f"Off-site media dependency found: {url} (referenced from {page_url})"
                print(f"ERROR: {dependency}")
                self.off_site_dependencies.append(dependency)
        else:
            # This is an on-site media file
            self.media_files.add(url)

    def _check_knightlab_media(self, full_url, path, page_url):
        """Check if media.knightlab.com asset exists locally and return local path"""
        # Remove /learncms/ prefix if present
        if path.startswith('/learncms/'):
            local_path = path[len('/learncms/'):]
        else:
            local_path = path.lstrip('/')

        # Check if file exists in static directory
        local_file = self.static_dir / local_path
        if local_file.exists():
            print(f"Found local asset: {local_file} for {full_url}")
            return f"/{local_path}"  # Return local path for URL rewriting
        else:
            missing = f"Missing local asset: {local_file} for {full_url} (referenced from {page_url})"
            print(f"ERROR: {missing}")
            self.missing_local_assets.append(missing)
            return None

    def process_html_content(self, content, page_url):
        """Process HTML content and validate dependencies"""
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='replace')

        # Rewrite media.knightlab.com URLs to local paths
        content = self._rewrite_knightlab_urls(content, page_url)

        # Validate media dependencies after rewriting
        self.validate_media_dependencies(content, page_url)

        return content

    def _rewrite_knightlab_urls(self, content, page_url):
        """Rewrite media.knightlab.com URLs to local static paths"""
        import re

        # Pattern to match media.knightlab.com URLs
        pattern = r'https?://media\.knightlab\.com/learncms/([^"\'\s>]+)'

        def replace_url(match):
            path = match.group(1)
            local_file = self.static_dir / path
            if local_file.exists():
                return f"/{path}"
            else:
                # Keep original URL if file doesn't exist locally (will be caught by validation)
                return match.group(0)

        return re.sub(pattern, replace_url, content)

    def save_content(self, relative_path, content, content_type='text/html'):
        """Save content to the output directory"""
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='replace')

        # Create the full path
        if relative_path == '' or relative_path == '/':
            file_path = self.output_dir / 'index.html'
        elif relative_path.endswith('/'):
            # Directory-style URLs get an index.html
            dir_path = self.output_dir / relative_path.strip('/')
            dir_path.mkdir(parents=True, exist_ok=True)
            file_path = dir_path / 'index.html'
        else:
            # File-style URLs
            file_path = self.output_dir / relative_path.lstrip('/')
            file_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Saving: {file_path}")

        if 'html' in content_type:
            # Process HTML content
            page_url = urljoin(self.base_url, relative_path)
            content = self.process_html_content(content, page_url)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def crawl_static_pages(self):
        """Crawl static template pages"""
        static_pages = [
            '/',           # homepage
            '/ask/',       # ask page
            '/404.html',   # 404 page
            '/500.html',   # 500 page
        ]

        for page in static_pages:
            if page not in self.crawled_urls:
                url = f"{self.base_url}{page}"
                content, content_type = self.fetch_url(url)
                if content:
                    self.save_content(page, content, content_type)
                    self.crawled_urls.add(page)

    def crawl_lesson_pages(self):
        """Crawl all published lesson pages"""
        lesson_slugs = self.get_lessons_from_api()
        print(f"Found {len(lesson_slugs)} published lessons")

        for slug in lesson_slugs:
            lesson_path = f"/lesson/{slug}/"
            if lesson_path not in self.crawled_urls:
                url = f"{self.base_url}{lesson_path}"
                content, content_type = self.fetch_url(url)
                if content:
                    self.save_content(lesson_path, content, content_type)
                    self.crawled_urls.add(lesson_path)

    def crawl_json_apis(self):
        """Crawl JSON API endpoints"""
        json_endpoints = [
            '/glossary.json',
            '/lesson.json',
            '/capsule.json'
        ]

        for endpoint in json_endpoints:
            if endpoint not in self.crawled_urls:
                url = f"{self.base_url}{endpoint}"
                content, content_type = self.fetch_url(url)
                if content:
                    self.save_content(endpoint, content, content_type)
                    self.crawled_urls.add(endpoint)

    def generate_site(self):
        """Generate the complete static site"""
        print(f"Generating static site from {self.base_url}")
        print(f"Output directory: {self.output_dir.absolute()}")
        print(f"Target domain: {self.domain}")

        start_time = time.time()

        # Crawl different types of content
        self.crawl_static_pages()
        self.crawl_lesson_pages()
        self.crawl_json_apis()

        # Report results
        end_time = time.time()
        print(f"\n--- Generation Results ---")
        print(f"Total pages crawled: {len(self.crawled_urls)}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"Media files found: {len(self.media_files)}")

        if self.failed_urls:
            print(f"\nFailed URLs ({len(self.failed_urls)}):")
            for url, error in self.failed_urls:
                print(f"  - {url}: {error}")

        # Check for off-site dependencies and missing local assets
        has_errors = False

        if self.off_site_dependencies:
            print(f"\n❌ Off-site dependencies found ({len(self.off_site_dependencies)}):")
            for dependency in self.off_site_dependencies:
                print(f"  - {dependency}")
            has_errors = True

        if self.missing_local_assets:
            print(f"\n❌ Missing local assets ({len(self.missing_local_assets)}):")
            for missing in self.missing_local_assets:
                print(f"  - {missing}")
            has_errors = True

        if has_errors:
            print(f"\n❌ GENERATION FAILED ❌")
            print("The static site cannot be fully portable with these issues.")
            print("Please fix these dependencies before generating a static site.")
            sys.exit(1)
        else:
            print(f"\n✅ SUCCESS: No off-site dependencies found!")
            print(f"Static site is fully portable and ready for deployment.")

        print(f"\nStatic site generated in: {self.output_dir.absolute()}")


def main():
    parser = argparse.ArgumentParser(description='Generate portable static site from learncms')
    parser.add_argument('--url', '-u',
                       default='https://learn.knightlab.com',
                       help='Base URL of the live site (default: https://learn.knightlab.com)')
    parser.add_argument('--output', '-o',
                       default='./static_site',
                       help='Output directory for static files (default: ./portable_static_site)')
    parser.add_argument('--timeout', '-t',
                       type=int, default=30,
                       help='Request timeout in seconds (default: 30)')

    args = parser.parse_args()

    # Generate the static site
    generator = StaticSiteGenerator(args.url, args.output)
    generator.generate_site()


if __name__ == '__main__':
    main()
