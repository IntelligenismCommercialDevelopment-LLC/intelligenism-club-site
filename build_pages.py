#!/usr/bin/env python3
"""
build_pages.py — Scan articles/ directory, extract metadata from HTML files,
generate pages.json, inject static <a href> links into index.html,
and generate sitemap.xml.

Usage: python3 build_pages.py

What it does:
1. Scans articles/*.html, extracts metadata (title, date, category, description)
2. Generates pages.json (backward compatible)
3. Reads index.html, finds marker comments, injects static links between them
   - category "doc"    → Articles column (article-card style)
   - category "update" → Updates column (update-item style)
   - category "release"→ Updates column (update-item style)
4. Writes updated index.html
5. Generates sitemap.xml with all pages and lastmod dates

Markers in index.html:
  <!-- BUILD_PAGES_ARTICLES_START -->
  ...injected content...
  <!-- BUILD_PAGES_ARTICLES_END -->

  <!-- BUILD_PAGES_UPDATES_START -->
  ...injected content...
  <!-- BUILD_PAGES_UPDATES_END -->
"""

import os
import re
import json
from datetime import date

ARTICLES_DIR = "articles"
PAGES_JSON = "pages.json"
INDEX_FILE = "index.html"
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
        date = extract_meta(content, 'article-date') or '1970-01-01'
        category = extract_meta(content, 'article-category') or 'update'
        description = extract_meta(content, 'article-description') or ''

        pages.append({
            'id': page_id,
            'title': title,
            'date': date,
            'category': category,
            'description': description
        })

    pages.sort(key=lambda p: p['date'], reverse=True)
    return pages


def generate_article_card(page):
    """Generate an article-card <a> block for doc category."""
    return (
        f'                    <a href="articles/{page["id"]}.html" class="article-card">\n'
        f'                        <div class="card-title">{page["title"]}</div>\n'
        f'                        <div class="card-date">{page["date"]}</div>\n'
        f'                        <div class="card-desc">{page["description"]}</div>\n'
        f'                    </a>\n'
    )


def generate_update_item(page):
    """Generate an update-item <a> block for update/release category."""
    return (
        f'                    <a href="articles/{page["id"]}.html" class="update-item">\n'
        f'                        <span class="update-date">{page["date"]}</span>\n'
        f'                        <div class="update-title">{page["title"]}</div>\n'
        f'                        <div class="update-desc">{page["description"]}</div>\n'
        f'                    </a>\n'
    )


def inject_into_index(pages):
    """Read index.html, inject static links between markers, write back."""
    if not os.path.isfile(INDEX_FILE):
        print(f"No {INDEX_FILE} found. Skipping injection.")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    # Separate pages by category
    articles = [p for p in pages if p['category'] == 'doc']
    updates = [p for p in pages if p['category'] in ('update', 'release')]

    # Generate HTML for articles
    articles_html = ""
    if articles:
        for p in articles:
            articles_html += generate_article_card(p)
    else:
        articles_html = '                    <p style="color: var(--text-dim); font-size: 0.8rem;">No articles yet.</p>\n'

    # Generate HTML for updates
    updates_html = ""
    if updates:
        for p in updates:
            updates_html += generate_update_item(p)
    else:
        updates_html = '                    <p style="color: var(--text-dim); font-size: 0.8rem;">No updates yet.</p>\n'

    # Inject articles
    articles_pattern = r'(<!-- BUILD_PAGES_ARTICLES_START -->\n).*?(<!-- BUILD_PAGES_ARTICLES_END -->)'
    articles_replacement = rf'\g<1>{articles_html}                    \2'
    html, count_a = re.subn(articles_pattern, articles_replacement, html, flags=re.DOTALL)
    if count_a == 0:
        print("WARNING: BUILD_PAGES_ARTICLES markers not found in index.html")

    # Inject updates
    updates_pattern = r'(<!-- BUILD_PAGES_UPDATES_START -->\n).*?(<!-- BUILD_PAGES_UPDATES_END -->)'
    updates_replacement = rf'\g<1>{updates_html}                    \2'
    html, count_u = re.subn(updates_pattern, updates_replacement, html, flags=re.DOTALL)
    if count_u == 0:
        print("WARNING: BUILD_PAGES_UPDATES markers not found in index.html")

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Injected {len(articles)} article(s) and {len(updates)} update(s) into {INDEX_FILE}.")


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

    # 1. Generate pages.json (backward compatible)
    with open(PAGES_JSON, 'w', encoding='utf-8') as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)
    print(f"Generated {PAGES_JSON} with {len(pages)} entries.")

    # 2. Inject static links into index.html
    inject_into_index(pages)

    # 3. Generate sitemap.xml
    generate_sitemap(pages)

    # 4. Summary
    for p in pages:
        print(f"  [{p['category']}] {p['date']} — {p['title']}")


if __name__ == '__main__':
    main()
