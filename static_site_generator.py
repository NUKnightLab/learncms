#!/usr/bin/env python3
"""
Static Site Generator for learncms Django Application

This script crawls the running Django application and generates static HTML files
that can be served by nginx or any other static web server.
"""

import os
import sys
import urllib.parse
import urllib.request
import json
import time
from pathlib import Path
import argparse
from urllib.error import HTTPError, URLError


class StaticSiteGenerator:
    def __init__(self, base_url, output_dir):
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.crawled_urls = set()
        self.failed_urls = []

    def fetch_url(self, url, timeout=30):
        """Fetch a URL and return the content"""
        try:
            print(f"Fetching: {url}")
            with urllib.request.urlopen(url, timeout=timeout) as response:
                if response.status == 200:
                    return response.read()
                else:
                    print(f"Warning: {url} returned status {response.status}")
                    return None
        except HTTPError as e:
            print(f"HTTP Error {e.code} for {url}: {e.reason}")
            self.failed_urls.append((url, f"HTTP {e.code}: {e.reason}"))
            return None
        except URLError as e:
            print(f"URL Error for {url}: {e.reason}")
            self.failed_urls.append((url, f"URL Error: {e.reason}"))
            return None
        except Exception as e:
            print(f"Unexpected error for {url}: {e}")
            self.failed_urls.append((url, f"Error: {e}"))
            return None


    def get_lessons_from_api(self):
        """Get all lesson slugs from the JSON API"""
        lessons_url = f"{self.base_url}/lesson.json"
        content = self.fetch_url(lessons_url)
        if content:
            try:
                lessons_data = json.loads(content.decode('utf-8'))
                # lessons_data is {title: {"slug": slug, "status": status}}
                return [data["slug"] for title, data in lessons_data.items()
                       if data.get("status") == "published"]
            except json.JSONDecodeError as e:
                print(f"Error parsing lessons JSON: {e}")
        return []

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
                content = self.fetch_url(url)
                if content:
                    self.save_content(page, content)
                    self.crawled_urls.add(page)

    def crawl_lesson_pages(self):
        """Crawl all published lesson pages"""
        lesson_slugs = self.get_lessons_from_api()
        print(f"Found {len(lesson_slugs)} published lessons")

        for slug in lesson_slugs:
            lesson_path = f"/lesson/{slug}/"
            if lesson_path not in self.crawled_urls:
                url = f"{self.base_url}{lesson_path}"
                content = self.fetch_url(url)
                if content:
                    self.save_content(lesson_path, content)
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
                content = self.fetch_url(url)
                if content:
                    self.save_content(endpoint, content, 'application/json')
                    self.crawled_urls.add(endpoint)

    def fix_web_component_paths(self, content):
        """Fix relative paths in HTML content for static site"""
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='replace')

        # Fix common static file references to use absolute paths
        # This ensures web components and other assets load correctly
        replacements = [
            # Fix script src paths
            ('src="/static/', 'src="/static/'),
            ('href="/static/', 'href="/static/'),
            # Ensure webcomponents load correctly
            ('src="{% static \'webcomponentsjs/webcomponents-lite.min.js\' %}"', 'src="/static/webcomponentsjs/webcomponents-lite.min.js"'),
            ('href="{% static \'webcomponents/webcomponents.html\' %}"', 'href="/static/webcomponents/webcomponents.html"'),
        ]

        for old, new in replacements:
            content = content.replace(old, new)

        return content

    def save_content(self, relative_path, content, content_type='text/html'):
        """Save content to the output directory"""
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='replace')

        # Fix web component paths for static site
        if content_type == 'text/html':
            content = self.fix_web_component_paths(content)

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
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def download_static_files(self):
        """Download static files (CSS, JS, images)"""
        print("Note: Static files (CSS, JS, images) should be collected using Django's collectstatic command")
        print("Run: python manage.py collectstatic --noinput")
        print("Then copy the collected static files to your nginx static directory")
        print("")
        print("IMPORTANT: For web components to work properly, ensure the following files are accessible:")
        print("- /static/webcomponentsjs/webcomponents-lite.min.js")
        print("- /static/webcomponents/webcomponents.html")
        print("- All Polymer components and dependencies")

    def generate_nginx_config(self):
        """Generate a basic nginx configuration"""
        nginx_config = f"""# Basic nginx configuration for learncms static site
server {{
    listen 80;
    server_name your-domain.com;
    root {self.output_dir.absolute()};
    index index.html;

    # Handle lesson URLs with trailing slashes
    location ~* ^/lesson/([a-z-]+)/?$ {{
        try_files /lesson/$1/index.html =404;
    }}

    # Handle static files (update paths as needed)
    location /static/ {{
        # Update this path to where you copy your collected static files
        alias /path/to/static/files/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}

    location /media/ {{
        # Update this path to where you copy your media files
        alias /path/to/media/files/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}

    # Handle other paths
    location / {{
        try_files $uri $uri/ $uri.html =404;
    }}

    # Custom error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /500.html;
}}"""

        nginx_config_path = self.output_dir / 'nginx.conf.example'
        with open(nginx_config_path, 'w') as f:
            f.write(nginx_config)
        print(f"Nginx configuration example saved to: {nginx_config_path}")

    def generate_site(self):
        """Generate the complete static site"""
        print(f"Generating static site from {self.base_url}")
        print(f"Output directory: {self.output_dir.absolute()}")

        start_time = time.time()

        # Crawl different types of content
        self.crawl_static_pages()
        self.crawl_lesson_pages()
        self.crawl_json_apis()

        # Generate additional files
        self.generate_nginx_config()
        self.download_static_files()

        # Report results
        end_time = time.time()
        print(f"\n--- Generation Complete ---")
        print(f"Total pages crawled: {len(self.crawled_urls)}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")

        if self.failed_urls:
            print(f"\nFailed URLs ({len(self.failed_urls)}):")
            for url, error in self.failed_urls:
                print(f"  - {url}: {error}")

        print(f"\nStatic site generated in: {self.output_dir.absolute()}")
        print("\nNext steps:")
        print("1. Run 'python manage.py collectstatic --noinput' to collect static files")
        print("2. Copy collected static files to your web server")
        print("3. Copy media files to your web server")
        print("4. Configure nginx using the example config file generated")


def main():
    parser = argparse.ArgumentParser(description='Generate static site from learncms Django app')
    parser.add_argument('--url', '-u',
                       default='http://localhost:8000',
                       help='Base URL of the running Django app (default: http://localhost:8000)')
    parser.add_argument('--output', '-o',
                       default='./static_site',
                       help='Output directory for static files (default: ./static_site)')
    parser.add_argument('--timeout', '-t',
                       type=int, default=30,
                       help='Request timeout in seconds (default: 30)')

    args = parser.parse_args()

    # Validate that the Django server is running
    try:
        urllib.request.urlopen(args.url, timeout=5)
    except Exception as e:
        print(f"Error: Cannot connect to Django server at {args.url}")
        print(f"Make sure your Django development server is running with: python manage.py runserver")
        sys.exit(1)

    # Generate the static site
    generator = StaticSiteGenerator(args.url, args.output)
    generator.generate_site()


if __name__ == '__main__':
    main()