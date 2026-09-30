#!/usr/bin/env python3
"""Validate a built site before it is published.

Checks, against the Hugo output directory (default: public/):

1. Every URL in scripts/legacy-urls.tsv still resolves. Those are the URLs
   docs.teramot.com published before this site replaced it; customers,
   contracts and search engines link to them.
2. Every internal link and asset reference (href/src starting with "/", or
   relative) in the generated HTML points at a file that exists.

Usage:

    python3 scripts/check_site.py [public]
"""

import html.parser
import pathlib
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEGACY = ROOT / "scripts/legacy-urls.tsv"

# Served by GitHub Pages or the browser, not by files in the build.
IGNORED_PREFIXES = ("//", "#", "mailto:", "tel:", "javascript:", "data:")


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link":
            # Only what the page loads; canonical/alternate point at absolute URLs.
            if attrs.get("rel") in ("stylesheet", "icon") and attrs.get("href"):
                self.links.append(attrs["href"])
            return
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append(attrs[name])


def resolve(public: pathlib.Path, page: pathlib.Path, link: str):
    """Return the file a link points at, or None when it is external or ignored."""
    if link.startswith(IGNORED_PREFIXES) or urllib.parse.urlsplit(link).scheme:
        return None
    path = urllib.parse.unquote(urllib.parse.urlsplit(link).path)
    if not path:
        return None
    if path.startswith("/"):
        target = public / path.lstrip("/")
    else:
        target = page.parent / path
    return target


def exists(target: pathlib.Path) -> bool:
    return target.is_file() or (target / "index.html").is_file()


def legacy_paths():
    for line in LEGACY.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        old, new = line.split("\t")
        yield old, new


def check(public: pathlib.Path) -> list[str]:
    errors = []

    for old, new in legacy_paths():
        if not (public / new.lstrip("/") / "index.html").is_file():
            errors.append(f"legacy URL {old} -> {new}: no page")

    for page in sorted(public.rglob("*.html")):
        parser = LinkParser()
        parser.feed(page.read_text(errors="replace"))
        for link in parser.links:
            target = resolve(public, page, link)
            if target is not None and not exists(target):
                errors.append(f"{page.relative_to(public)}: broken link {link}")

    return errors


def main() -> int:
    public = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "public")
    if not public.is_dir():
        print(f"{public} is not a directory; build the site first", file=sys.stderr)
        return 2
    errors = check(public)
    for e in errors:
        print(e, file=sys.stderr)
    pages = sum(1 for _ in public.rglob("*.html"))
    print(f"checked {pages} pages: {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
