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
5. **Magnifying glass overlays not working**: Web components need proper setup (see below)
6. **Callout blocks show placeholder icons**: Emoji font not loading correctly (see below)

### Fixing Web Component Issues (Magnifying Glass Overlays)

The magnifying glass zoom functionality uses Polymer web components. If the overlays show only a sliver or don't work at all, follow these steps:

#### Step 1: Use the Debug Tool
```bash
# Check if required files exist
python debug_static_site.py check --static-dir ./static

# Fix HTML template tags that break web components
python debug_static_site.py fix --site-dir ./static_site

# Diagnose a specific page
python debug_static_site.py diagnose --file ./static_site/lesson/some-lesson/index.html
```

#### Step 2: Manual Fixes
If the debug tool doesn't fix everything, check these manually:

1. **Ensure web components are loaded in HTML head**:
   ```html
   <script src="/static/webcomponentsjs/webcomponents-lite.min.js"></script>
   <link rel="import" href="/static/webcomponents/webcomponents.html">
   ```

2. **Check that static files exist**:
   - `/static/webcomponentsjs/webcomponents-lite.min.js`
   - `/static/webcomponents/webcomponents.html`
   - All Polymer component files

3. **Remove Django template tags from static HTML**:
   - Replace `{% static 'file.js' %}` with `/static/file.js`
   - Remove `{% load staticfiles %}` from HTML files

#### Step 3: Verify Component Loading
Open browser developer tools and check:
- No 404 errors for `/static/webcomponents*` files
- No JavaScript errors related to Polymer
- `<zooming-image>` elements are properly defined

#### Common Error Messages
- "webcomponents-lite.min.js:1 Failed to load": Static files not copied correctly
- "Uncaught TypeError: Cannot read property": Django template tags not fixed
- Overlay shows only a sliver: CSS z-index conflicts or missing component definitions

### Fixing Callout Block Emoji Issues

If callout blocks (like "Danger, danger!" messages) show placeholder circle icons instead of proper emojis:

#### The Problem
Info blocks use a custom emoji font (`EmojiSymbols-Regular.woff`) that may not be loading correctly in the static site.

#### The Solution
```bash
# 1. Check if emoji font exists
python debug_static_site.py check --static-dir ./static

# 2. Fix font paths in static files
python debug_static_site.py fix --site-dir ./static_site

# 3. Verify the emoji font is in the right place
ls ./static/css/EmojiSymbols-Regular.woff
```

#### Manual Fix
If the font file is missing:
1. **Copy the emoji font** from your Django static files to `/static/css/EmojiSymbols-Regular.woff`
2. **Update web component CSS** to use the correct path:
   ```css
   @font-face {
     font-family: "EmojiSymbols";
     src: url('/static/css/EmojiSymbols-Regular.woff') format('woff');
   }
   ```
3. **Check browser console** for any remaining font loading errors

#### Alternative Solution
If the emoji font continues to cause issues, you can modify the info-block component to use system emojis instead by removing the custom font family.

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