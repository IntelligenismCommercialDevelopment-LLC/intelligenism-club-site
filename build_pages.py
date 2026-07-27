#!/usr/bin/env python3
"""
build_pages.py — Scan articles/ directory, extract metadata from HTML files,
and generate pages.json + sitemap.xml.

Usage: python3 build_pages.py

What it does:
1. Scans articles/*.html, extracts metadata (title, date, category, description)
2. Generates pages.json (page inventory, sorted newest first)
3. Generates sitemap.xml (homepage + every article page, with lastmod dates)

NOTE: index.html is hand-maintained. The homepage no longer auto-injects article
cards — derived-use-case cards are edited directly in index.html (see the card
template comment there). This script therefore does NOT touch index.html.
"""

import os
import re
import json
from datetime import date

ARTICLES_DIR = "articles"
PAGES_JSON = "pages.json"
SITEMAP_FILE = "sitemap.xml"
SITE_URL = "https://intelligenism.club"


def extract_meta(html_content, name):
    """Extract content from <meta name="..." content="...">"""
    pattern = rf'<meta\s+name="{name}"\s+content="([^"]*)"'
    match = re.search(pattern, html_content, re.IGNORECASE)
    return match.group(1) if match else None


def extract_title(html_content):
    """Extract content from <title>...</title>"""
    match = re.search(r'<title>([^<]*)</title>', html_content, re.IGNORECASE)
    return match.group(1) if match else None


def scan_articles():
    """Scan articles/ for .html files and extract metadata."""
    if not os.path.isdir(ARTICLES_DIR):
        print(f"No {ARTICLES_DIR}/ directory found. Creating empty {PAGES_JSON}.")
        return []

    pages = []
    for filename in sorted(os.listdir(ARTICLES_DIR)):
        if not filename.endswith('.html'):
            continue

        filepath = os.path.join(ARTICLES_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        page_id = filename.replace('.html', '')
        title = extract_title(content) or page_id
        date_str = extract_meta(content, 'article-date') or '1970-01-01'
        category = extract_meta(content, 'article-category') or 'doc'
        description = extract_meta(content, 'article-description') or ''

        pages.append({
            'id': page_id,
            'title': title,
            'date': date_str,
            'category': category,
            'description': description
        })

    pages.sort(key=lambda p: p['date'], reverse=True)
    return pages


def generate_sitemap(pages):
    """Generate sitemap.xml with homepage + all article pages."""
    today = date.today().isoformat()

    urls = []
    # Homepage
    urls.append(f'  <url>\n    <loc>{SITE_URL}/</loc>\n    <lastmod>{today}</lastmod>\n  </url>')

    # Article pages
    for p in pages:
        lastmod = p['date'] if p['date'] != '1970-01-01' else today
        urls.append(
            f'  <url>\n'
            f'    <loc>{SITE_URL}/articles/{p["id"]}.html</loc>\n'
            f'    <lastmod>{lastmod}</lastmod>\n'
            f'  </url>'
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(urls) + '\n'
        '</urlset>\n'
    )

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(sitemap)

    print(f"Generated {SITEMAP_FILE} with {len(urls)} URLs.")


def main():
    pages = scan_articles()

    # 1. Generate pages.json (page inventory)
    with open(PAGES_JSON, 'w', encoding='utf-8') as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)
    print(f"Generated {PAGES_JSON} with {len(pages)} entries.")

    # 2. Generate sitemap.xml
    generate_sitemap(pages)

    # 3. Summary
    for p in pages:
        print(f"  [{p['category']}] {p['date']} — {p['title']}")


if __name__ == '__main__':
    main()
