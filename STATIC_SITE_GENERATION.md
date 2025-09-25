# Static Site Generation for learncms

This document explains how to convert your learncms Django application to a static site that can be served by nginx or any other static web server.

## Overview

The `static_site_generator.py` script crawls your running Django application and generates static HTML files for all public pages, including:

- Homepage (`/`)
- All published lesson pages (`/lesson/<slug>/`)
- Static pages (`/ask/`, `/404.html`, `/500.html`)
- JSON API endpoints (`/glossary.json`, `/lesson.json`, `/capsule.json`)

## Prerequisites

1. Your Django application must be running and accessible
2. Python 3.6+ (uses only standard library modules)
3. All lessons you want to include should have `status='published'`

## Usage

### Basic Usage

1. Start your Django development server:
   ```bash
   python manage.py runserver
   ```

2. Run the static site generator:
   ```bash
   python static_site_generator.py
   ```

This will create a `static_site` directory with all the generated HTML files.

### Advanced Usage

```bash
# Generate from a different URL
python static_site_generator.py --url http://your-domain.com

# Specify custom output directory
python static_site_generator.py --output /path/to/output

# Adjust timeout for slow pages
python static_site_generator.py --timeout 60

# Combine options
python static_site_generator.py -u http://localhost:8080 -o ./my_static_site -t 45
```

### Options

- `--url, -u`: Base URL of the running Django app (default: `http://localhost:8000`)
- `--output, -o`: Output directory for static files (default: `./static_site`)
- `--timeout, -t`: Request timeout in seconds (default: 30)

## Complete Deployment Process

### Step 1: Generate Static HTML
```bash
python static_site_generator.py --output ./static_site
```

### Step 2: Collect Static Assets
```bash
python manage.py collectstatic --noinput
```

### Step 3: Prepare Files for Deployment
```bash
# Copy static files (CSS, JS, etc.)
cp -r /path/to/collected/static ./static_site/static/

# Copy media files (images, uploads, etc.)
cp -r /path/to/media ./static_site/media/
```

### Step 4: Configure nginx

The script generates an example nginx configuration file (`nginx.conf.example`) in the output directory. Use this as a starting point:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/static_site;
    index index.html;

    # Handle lesson URLs with trailing slashes
    location ~* ^/lesson/([a-z-]+)/?$ {
        try_files /lesson/$1/index.html =404;
    }

    # Handle static files
    location /static/ {
        alias /path/to/static_site/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/static_site/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Handle other paths
    location / {
        try_files $uri $uri/ $uri.html =404;
    }

    # Custom error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /500.html;
}
```

### Step 5: Deploy to Your Server
```bash
# Upload files to your server
rsync -avz ./static_site/ user@server:/var/www/learncms/

# Configure nginx
sudo cp nginx.conf.example /etc/nginx/sites-available/learncms
sudo ln -s /etc/nginx/sites-available/learncms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Output Structure

The generated static site will have the following structure:

```
static_site/
├── index.html                 # Homepage
├── lesson/
│   ├── lesson-slug-1/
│   │   └── index.html         # Lesson detail page
│   └── lesson-slug-2/
│       └── index.html
├── ask/
│   └── index.html             # Ask page
├── 404.html                   # 404 error page
├── 500.html                   # 500 error page
├── glossary.json              # Glossary API
├── lesson.json                # Lessons API
├── capsule.json               # Capsules API
├── nginx.conf.example         # Example nginx config
├── static/                    # Static assets (after collectstatic)
│   ├── css/
│   ├── js/
│   └── images/
└── media/                     # Media files
    └── uploads/
```

## Troubleshooting

### Common Issues

1. **Connection refused**: Make sure your Django server is running
2. **404 errors**: Check that lessons have `status='published'`
3. **Missing static files**: Run `collectstatic` and copy files to output directory
4. **Timeout errors**: Increase timeout with `--timeout` option

### Checking Generated Content

```bash
# Verify HTML pages were generated
find static_site -name "*.html" | wc -l

# Check for any failed URLs
python static_site_generator.py 2>&1 | grep "Error\|Failed"

# Test locally with Python's built-in server
cd static_site
python -m http.server 8080
# Visit http://localhost:8080
```

## Automation

You can automate the entire process with a shell script:

```bash
#!/bin/bash
# generate_static_site.sh

set -e

echo "Starting static site generation..."

# Start Django server in background
python manage.py runserver &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Generate static site
python static_site_generator.py --output ./static_site

# Collect static files
python manage.py collectstatic --noinput

# Copy static files to output
cp -r path/to/collected/static ./static_site/static/
cp -r path/to/media ./static_site/media/

# Stop Django server
kill $SERVER_PID

echo "Static site generation complete!"
echo "Files are ready in: ./static_site"
```

## Notes

- Only published lessons (`status='published'`) are included in the static site
- The script preserves the URL structure of your Django app
- JSON API endpoints are preserved for any client-side functionality
- Custom error pages (404, 500) are included
- The script is safe to run multiple times (overwrites existing files)