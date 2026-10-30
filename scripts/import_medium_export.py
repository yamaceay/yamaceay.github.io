#!/usr/bin/env python3
"""One-time import of a Medium "Download your information" export into
_posts/. Not part of the daily sync (scripts/sync_medium.py handles
that going forward) — run this by hand when you have a fresh export.

Usage: python3 scripts/import_medium_export.py /path/to/export/posts

Skips anything already mirrored (matched by original_url) and anything
matching _data/site.yml's blog.exclude. Recovers GitHub Gist code
embeds via the `gh` CLI, since the static export only contains a
<script src="https://gist.github.com/...js"> placeholder with no text.
"""
import html
import os
import re
import subprocess
import sys

import yaml
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR = os.path.join(ROOT, "_posts")
SITE_DATA = os.path.join(ROOT, "_data", "site.yml")


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "post"


def story_id(url):
    """Medium's stable per-story hex id, regardless of which domain/slug
    variant the URL uses (custom domain, medium.com/@user, pub domain,
    with/without ?source= query)."""
    m = re.search(r"([0-9a-f]{6,16})(?:\?.*)?$", url)
    return m.group(1) if m else url


def existing_story_ids():
    ids = set()
    if not os.path.isdir(POSTS_DIR):
        return ids
    for name in os.listdir(POSTS_DIR):
        if not name.endswith((".md", ".markdown")):
            continue
        with open(os.path.join(POSTS_DIR, name), encoding="utf-8") as f:
            text = f.read(2000)
        m = re.search(r'^original_url:\s*"([^"]+)"', text, re.MULTILINE)
        if m:
            ids.add(story_id(m.group(1)))
    return ids


def curation_lists():
    with open(SITE_DATA, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    blog = data.get("blog") or {}
    return blog.get("include") or [], blog.get("exclude") or []


def is_visible(link, include_patterns, exclude_patterns):
    if include_patterns:
        return any(p and p in link for p in include_patterns)
    return not any(p and p in link for p in exclude_patterns)


def escape_yaml(text):
    return text.replace("\\", "\\\\").replace('"', '\\"')


_gist_cache = {}


def fetch_gist(gist_id):
    if gist_id in _gist_cache:
        return _gist_cache[gist_id]
    try:
        result = subprocess.run(
            ["gh", "gist", "view", gist_id],
            capture_output=True, text=True, timeout=20, check=True,
        )
        out = result.stdout
    except Exception as e:
        print(f"  ! failed to fetch gist {gist_id}: {e}", file=sys.stderr)
        out = None
    _gist_cache[gist_id] = out
    return out


def clean_inline(tag):
    out = []
    for child in tag.children:
        if isinstance(child, NavigableString):
            out.append(html.escape(str(child)))
        elif isinstance(child, Tag):
            if child.name == "a":
                href = child.get("href") or child.get("data-href") or ""
                out.append(f'<a href="{html.escape(href, quote=True)}">{clean_inline(child)}</a>')
            elif child.name == "br":
                out.append("<br/>")
            elif child.name in ("strong", "em", "code", "sup", "sub"):
                out.append(f"<{child.name}>{clean_inline(child)}</{child.name}>")
            else:
                out.append(clean_inline(child))
    return "".join(out)


def process_pre(pre_tag):
    code = pre_tag.find("code")
    target = code if code else pre_tag
    parts = []
    for child in target.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag) and child.name == "br":
            parts.append("\n")
        else:
            parts.append(child.get_text())
    text = "".join(parts)
    return f"<pre><code>{html.escape(text)}</code></pre>"


def process_gist_figure(figure_tag):
    script = figure_tag.find("script", src=True)
    if not script:
        return ""
    m = re.search(r"gist\.github\.com/[^/]+/([0-9a-f]+)", script["src"])
    if not m:
        return ""
    code = fetch_gist(m.group(1))
    if not code:
        return ""
    return f"<pre><code>{html.escape(code.strip())}</code></pre>"


def process_mixtape(div_tag):
    a = div_tag.find("a", href=True)
    if not a:
        return ""
    href = a["href"]
    strong = a.find("strong")
    title = strong.get_text(strip=True) if strong else a.get_text(strip=True)
    if not title:
        return ""
    return f'<p><a href="{html.escape(href, quote=True)}">{html.escape(title)}</a></p>'


def process_body(body_section):
    parts = []
    title_skipped = False
    for el in body_section.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6", "p", "pre", "figure", "ul", "ol", "blockquote", "div"],
        recursive=True,
    ):
        classes = el.get("class") or []
        if el.name == "div":
            if "graf--mixtapeEmbed" in classes:
                html_piece = process_mixtape(el)
                if html_piece:
                    parts.append(html_piece)
            continue
        if el.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if "graf--title" in classes and not title_skipped:
                title_skipped = True
                continue
            text = el.get_text(strip=True)
            if text:
                parts.append(f"<h4>{html.escape(text)}</h4>")
        elif el.name == "pre":
            parts.append(process_pre(el))
        elif el.name == "p":
            if "graf--pre" in classes:
                continue
            inner = clean_inline(el).strip()
            if inner:
                parts.append(f"<p>{inner}</p>")
        elif el.name == "figure":
            if "graf--iframe" in classes or el.find("script", src=re.compile("gist")):
                code_html = process_gist_figure(el)
                if code_html:
                    parts.append(code_html)
                continue
            img = el.find("img")
            if not img:
                continue
            src = img.get("src", "")
            src = re.sub(r"/max/\d+/", "/max/1400/", src)
            fig = f'<figure><img alt="" src="{html.escape(src, quote=True)}" />'
            cap = el.find("figcaption")
            if cap:
                cap_html = clean_inline(cap).strip()
                if cap_html:
                    fig += f"<figcaption>{cap_html}</figcaption>"
            fig += "</figure>"
            parts.append(fig)
        elif el.name in ("ul", "ol"):
            items = []
            for li in el.find_all("li", recursive=False):
                li_html = clean_inline(li).strip()
                if li_html:
                    items.append(f"<li>{li_html}</li>")
            if items:
                parts.append(f"<{el.name}>{''.join(items)}</{el.name}>")
        elif el.name == "blockquote":
            inner = clean_inline(el).strip()
            if inner:
                parts.append(f"<blockquote>{inner}</blockquote>")
    return "".join(parts)


def strip_tags_for_excerpt(content_html):
    text = re.sub(r"(</(p|h[1-6]|li|blockquote|figcaption)>|<br\s*/?>)", " ", content_html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def convert_one(path):
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    h1 = soup.find("h1", class_=lambda c: c and "p-name" in c)
    title = h1.get_text(strip=True) if h1 else (soup.title.get_text(strip=True) if soup.title else "Untitled")

    canonical_a = soup.find("a", class_=lambda c: c and "p-canonical" in c)
    original_url = canonical_a["href"] if canonical_a else None
    if not original_url:
        return None

    time_el = soup.find("time", class_=lambda c: c and "dt-published" in c)
    date_raw = time_el["datetime"] if time_el else None
    if date_raw:
        date_iso = re.sub(r"\.\d+Z$", "+00:00", date_raw)
        if date_iso.endswith("Z"):
            date_iso = date_iso[:-1] + "+00:00"
    else:
        date_iso = "1970-01-01T00:00:00+00:00"
    date_str = date_iso[:10]

    body_section = soup.find("section", attrs={"data-field": "body"})
    if not body_section:
        return None
    content = process_body(body_section)
    if not content.strip():
        return None

    excerpt = strip_tags_for_excerpt(content)[:200]

    return {
        "title": title,
        "date_iso": date_iso,
        "date_str": date_str,
        "original_url": original_url,
        "content": content,
        "excerpt": excerpt,
    }


def write_post(entry):
    slug = slugify(entry["title"])
    path = os.path.join(POSTS_DIR, f"{entry['date_str']}-{slug}.md")
    suffix = 2
    while os.path.exists(path):
        path = os.path.join(POSTS_DIR, f"{entry['date_str']}-{slug}-{suffix}.md")
        suffix += 1

    front_matter = "\n".join([
        "---",
        "layout: post",
        f'title: "{escape_yaml(entry["title"])}"',
        f"date: {entry['date_iso']}",
        f'original_url: "{entry["original_url"]}"',
        "tags: []",
        f'excerpt: "{escape_yaml(entry["excerpt"])}"',
        "---",
        "",
        "{% raw %}",  # article content can contain literal {{ }} (e.g. set notation)
        entry["content"],  # which Liquid would otherwise try to parse as template syntax
        "{% endraw %}",
        "",
    ])
    with open(path, "w", encoding="utf-8") as f:
        f.write(front_matter)
    return path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/import_medium_export.py /path/to/export/posts")
        sys.exit(1)
    posts_dir = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    seen = existing_story_ids()
    include, exclude = curation_lists()
    os.makedirs(POSTS_DIR, exist_ok=True)

    created, skipped_seen, skipped_excluded, skipped_empty = 0, 0, 0, 0

    for name in sorted(os.listdir(posts_dir)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(posts_dir, name)
        entry = convert_one(path)
        if entry is None:
            print(f"SKIP (unparseable): {name}")
            skipped_empty += 1
            continue
        link = entry["original_url"]
        if story_id(link) in seen:
            skipped_seen += 1
            continue
        if not is_visible(link, include, exclude):
            print(f"SKIP (excluded): {entry['title']}")
            skipped_excluded += 1
            continue
        if dry_run:
            print(f"WOULD CREATE: {entry['date_str']} - {entry['title']}")
        else:
            out_path = write_post(entry)
            print(f"Created {out_path}")
        created += 1

    print(f"\nDone. {created} {'would be ' if dry_run else ''}created, "
          f"{skipped_seen} already mirrored, {skipped_excluded} excluded, "
          f"{skipped_empty} unparseable.")


if __name__ == "__main__":
    main()
