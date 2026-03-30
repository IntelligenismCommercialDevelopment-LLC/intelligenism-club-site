#!/usr/bin/env python3
"""
build_pages.py — Scan articles/ directory, extract metadata from HTML files,
generate pages.json for the index page.

Usage: python3 build_pages.py
"""

import os
import re
import json

ARTICLES_DIR = "articles"
OUTPUT_FILE = "pages.json"


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
        print(f"No {ARTICLES_DIR}/ directory found. Creating empty {OUTPUT_FILE}.")
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

    # sort by date descending
    pages.sort(key=lambda p: p['date'], reverse=True)
    return pages


def main():
    pages = scan_articles()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)
    print(f"Generated {OUTPUT_FILE} with {len(pages)} entries.")
    for p in pages:
        print(f"  [{p['category']}] {p['date']} — {p['title']}")


if __name__ == '__main__':
    main()
