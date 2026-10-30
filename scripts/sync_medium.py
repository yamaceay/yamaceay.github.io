#!/usr/bin/env python3
"""Mirror new posts from the Medium RSS feed into Jekyll _posts/.

Run daily by .github/workflows/sync-medium.yml. Only ADDS new posts —
never touches an already-mirrored file, so manual edits are safe.
"""
import html
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

import yaml

FEED_URL = "https://medium.com/feed/@yamaceay"
ROOT = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR = os.path.join(ROOT, "_posts")
SITE_DATA = os.path.join(ROOT, "_data", "site.yml")
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"


def curation_lists():
    with open(SITE_DATA, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    blog = data.get("blog") or {}
    return blog.get("include") or [], blog.get("exclude") or []


def is_visible(link, include_patterns, exclude_patterns):
    # `include` wins outright when non-empty: whitelist mode.
    if include_patterns:
        return any(p and p in link for p in include_patterns)
    return not any(p and p in link for p in exclude_patterns)


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "post"


def strip_tags(text):
    text = re.sub(r"(</(p|h[1-6]|li|div|blockquote|figcaption)>|<br\s*/?>)", " ", text, flags=re.IGNORECASE)
    return re.sub(r"<[^>]+>", "", text)


def strip_tracking_pixel(content):
    return re.sub(r'<img[^>]*medium\.com/_/stat[^>]*>', "", content)


def existing_original_urls():
    urls = set()
    if not os.path.isdir(POSTS_DIR):
        return urls
    for name in os.listdir(POSTS_DIR):
        if not name.endswith((".md", ".markdown", ".html")):
            continue
        with open(os.path.join(POSTS_DIR, name), encoding="utf-8") as f:
            text = f.read(2000)
        m = re.search(r'^original_url:\s*"([^"]+)"', text, re.MULTILINE)
        if m:
            urls.add(m.group(1))
    return urls


def fetch_feed():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def escape_yaml(text):
    return text.replace("\\", "\\\\").replace('"', '\\"')


def main():
    os.makedirs(POSTS_DIR, exist_ok=True)
    seen = existing_original_urls()
    include, exclude = curation_lists()
    root = ET.fromstring(fetch_feed())
    created = 0
    skipped = 0

    for item in root.findall("./channel/item"):
        link = (item.findtext("link") or "").split("?")[0]
        if not link or link in seen:
            continue
        if not is_visible(link, include, exclude):
            skipped += 1
            print(f"Skipped (curated out): {link}")
            continue

        title = (item.findtext("title") or "Untitled").strip()
        pub_date = item.findtext("pubDate")
        date = parsedate_to_datetime(pub_date) if pub_date else None
        categories = [c.text.strip() for c in item.findall("category") if c.text]
        content_el = item.find(f"{{{CONTENT_NS}}}encoded")
        content = (content_el.text or "").strip() if content_el is not None else ""
        if not content:
            continue  # skip the feed's own "profile" entry etc.
        content = strip_tracking_pixel(content).strip()

        excerpt = html.unescape(strip_tags(content)).strip()
        excerpt = re.sub(r"\s+", " ", excerpt)[:200]

        slug = slugify(title)
        date_str = date.strftime("%Y-%m-%d") if date else "1970-01-01"
        path = os.path.join(POSTS_DIR, f"{date_str}-{slug}.md")
        suffix = 2
        while os.path.exists(path):
            path = os.path.join(POSTS_DIR, f"{date_str}-{slug}-{suffix}.md")
            suffix += 1

        tags_yaml = (
            "[" + ", ".join(f'"{escape_yaml(c)}"' for c in categories) + "]"
            if categories
            else "[]"
        )
        date_iso = date.isoformat() if date else "1970-01-01T00:00:00+00:00"

        front_matter = "\n".join([
            "---",
            "layout: post",
            f'title: "{escape_yaml(title)}"',
            f"date: {date_iso}",
            f'original_url: "{link}"',
            f"tags: {tags_yaml}",
            f'excerpt: "{escape_yaml(excerpt)}"',
            "---",
            "",
            "{% raw %}",  # Medium content can contain literal {{ }} (e.g. set notation)
            content,      # which Liquid would otherwise try to parse as template syntax
            "{% endraw %}",
            "",
        ])

        with open(path, "w", encoding="utf-8") as f:
            f.write(front_matter)

        created += 1
        print(f"Created {path}")

    print(f"Done. {created} new post(s), {skipped} curated out.")


if __name__ == "__main__":
    main()
