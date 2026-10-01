#!/usr/bin/env python3
"""Copy the product docs and the release notes from teramot-aleph into this site.

teramot-aleph is the source of truth: its CI checks every page of public-docs/
against the code, so what this writes is gitignored here and never edited by hand.

  public-docs/**/*.md                  -> content/product/   (adapted for Hugo)
  public-docs/**/<images>              -> static/product/
  frontend/public/release-notes.json   -> data/aleph/release_notes.json (/changelog/)

The aleph checkout defaults to a sibling of this repo (../teramot-aleph); CI passes
--aleph with the ref it checked out.

Usage: python3 scripts/sync_aleph.py [--aleph PATH]
"""

import argparse
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "product"
STATIC = ROOT / "static" / "product"
DATA = ROOT / "data" / "aleph" / "release_notes.json"
URL_BASE = "/product"
IMAGES = {".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"}

# Sidebar title and order of each public-docs/ folder. A folder missing here fails
# the sync rather than showing up under its directory name.
SECTIONS = {
    "concepts": ("Concepts", 10),
    "connect-data": ("Connect your data", 20),
    "use-the-app": ("Use the app", 30),
    "mcp": ("AI assistants", 40),
}

# URLs this site published before the pages came from aleph, kept alive as redirects
# (scripts/legacy-urls.tsv fails the build if one stops resolving).
ALIASES = {
    "mcp/_index.md": ["/api/"],
    "mcp/overview.md": ["/api/intro/"],
    "mcp/authentication.md": ["/api/authentication/"],
    "mcp/connect-clients.md": ["/api/connect-clients/"],
    "mcp/tools-reference.md": ["/api/tools-reference/"],
}

MARKER = re.compile(r"^\[//\]: # \((.+)\)$")
HEADING = re.compile(r"^(#+) (.+)$")
LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCE = re.compile(r"^\s*```")


def fail(msg):
    sys.exit(f"sync_aleph: {msg}")


def slug(heading):
    """The anchor Hugo gives a heading, as aleph's public-docs-check.sh computes it."""
    return re.sub(r"[^a-z0-9 _-]", "", heading.lower()).replace(" ", "-")


def page_url(rel):
    """public-docs/ path of a page -> its URL here: one directory per page."""
    path = rel[: -len(".md")]
    path = path[: -len("index")] if path == "index" or path.endswith("/index") else path
    path = path.strip("/")
    return f"{URL_BASE}/{path}/" if path else f"{URL_BASE}/"


def split_front_matter(text, rel):
    if not text.startswith("---\n"):
        fail(f"{rel} has no front matter")
    head, _, body = text[4:].partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            meta[m[1]] = m[2].strip().strip("\"'")
    return meta, body


def front_matter(meta, dest=None):
    """aleph's keys -> Hugo's. covers: and search_weight: only mean something in aleph."""
    out = {"title": meta["title"]}
    if meta.get("description"):
        out["description"] = meta["description"]
    if meta.get("sidebar_position"):
        out["weight"] = int(meta["sidebar_position"])
    if meta.get("sidebar_label"):
        out["linkTitle"] = meta["sidebar_label"]
    if dest in ALIASES:
        out["aliases"] = ALIASES[dest]
    # json.dumps writes a double-quoted YAML scalar, safe for any title.
    return "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in out.items()) + "---\n"


def resolve_link(target, rel):
    """A relative link of the page at `rel` -> a root-relative URL of this site."""
    if re.match(r"^[a-z]+:", target) or target.startswith(("#", "/")):
        return target
    path, _, anchor = target.partition("#")
    parts = pathlib.PurePosixPath(rel).parent.joinpath(path).parts
    stack = []
    for p in parts:
        if p == "..":
            if not stack:
                fail(f"{rel} links outside public-docs/: {target}")
            stack.pop()
        elif p not in (".", ""):
            stack.append(p)
    resolved = "/".join(stack)
    url = page_url(resolved) if resolved.endswith(".md") else f"{URL_BASE}/{resolved}"
    return url + (f"#{anchor}" if anchor else "")


def render_tabs(lines):
    """A tabs block, one tab per heading at its first heading level, as Hextra tabs.

    Each tab opens with an anchor named like its heading, so a link to the heading
    (and search_docs, which links there) still lands on it; static/js/product-tabs.js
    opens the tab that holds the anchor.
    """
    level = None
    tabs = []
    for line in lines:
        m = HEADING.match(line)
        if m and (level is None or len(m[1]) == level):
            level = len(m[1])
            tabs.append((m[2], []))
        elif tabs:
            tabs[-1][1].append(line)
        elif line.strip():
            fail("a tabs block must open with a heading")
    out = ["{{< tabs >}}"]
    for name, body in tabs:
        out.append(f'{{{{< tab name={json.dumps(name)} >}}}}')
        out.append(f'<span id="{slug(name)}" class="tm-tab-anchor"></span>')
        out.append("")
        out.extend(body)
        out.append("{{< /tab >}}")
    out.append("{{< /tabs >}}")
    return out


def convert_body(body, rel):
    lines = body.split("\n")
    # The title is rendered from front matter; the page's own # heading would repeat it.
    for i, line in enumerate(lines):
        if line.strip():
            if line.startswith("# "):
                del lines[i]
                if i < len(lines) and not lines[i].strip():
                    del lines[i]
            break

    out, block, block_kind, fenced, where = [], [], None, False, False
    for line in lines:
        if FENCE.match(line):
            fenced = not fenced
        if not fenced:
            line = LINK.sub(lambda m: "](" + resolve_link(m[1], rel) + ")", line)
            marker = MARKER.match(line)
            if marker:
                name = marker[1]
                if name in ("tabs:start", "cards:start"):
                    block, block_kind = [], name.split(":")[0]
                elif name == "tabs:end":
                    out.extend(render_tabs(block))
                    block_kind = None
                elif name == "cards:end":
                    out.extend(["{{< link-cards >}}", *block, "{{< /link-cards >}}"])
                    block_kind = None
                # public-docs-sync:<id> markers only matter to aleph's generator.
                continue
            # A paragraph opening with **Where:** says where the page's feature is; the
            # site sets it apart as a quote.
            if line.startswith("**Where:**"):
                where = True
            elif not line.strip():
                where = False
            if where:
                line = "> " + line
        (block if block_kind else out).append(line)
    if block_kind:
        fail(f"{rel}: {block_kind}:start never closed")
    return "\n".join(out)


def sync_docs(src):
    for target in (CONTENT, STATIC):
        shutil.rmtree(target, ignore_errors=True)
    dirs = set()
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src).as_posix()
        if path.is_dir() or any(p.startswith(".") for p in rel.split("/")):
            continue
        if path.suffix in IMAGES:
            (STATIC / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, STATIC / rel)
        elif path.suffix == ".md":
            meta, body = split_front_matter(path.read_text(), rel)
            name = "_index.md" if path.name == "index.md" else path.name
            dest = CONTENT / pathlib.PurePosixPath(rel).parent / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            fm = front_matter(meta, dest.relative_to(CONTENT).as_posix())
            if rel == "index.md":
                # The section root: every page under it is a docs page with its own sidebar.
                fm = fm[:-4] + "cascade:\n  type: docs\n---\n"
            dest.write_text(fm + "\n" + convert_body(body, rel))
            if "/" in rel:
                dirs.add(rel.split("/")[0])
    if not (CONTENT / "_index.md").exists():
        fail(f"{src} has no index.md")
    for d in sorted(dirs):
        if d not in SECTIONS:
            fail(f"public-docs/{d}/ has no sidebar title: add it to SECTIONS in {__file__}")
        title, weight = SECTIONS[d]
        (CONTENT / d / "_index.md").write_text(
            front_matter({"title": title, "sidebar_position": weight}, f"{d}/_index.md"))


def sync_release_notes(src):
    DATA.parent.mkdir(parents=True, exist_ok=True)
    notes = json.loads(src.read_text())
    if not isinstance(notes.get("releases"), list):
        fail(f"{src} has no releases list")
    DATA.write_text(json.dumps(notes, ensure_ascii=False, indent=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--aleph", type=pathlib.Path, default=ROOT.parent / "teramot-aleph",
                        help="teramot-aleph checkout (default: ../teramot-aleph)")
    args = parser.parse_args()
    docs = args.aleph / "public-docs"
    notes = args.aleph / "frontend" / "public" / "release-notes.json"
    for p in (docs, notes):
        if not p.exists():
            fail(f"{p} does not exist. Clone teramot-aleph next to this repo, or pass --aleph.")
    sync_docs(docs)
    sync_release_notes(notes)
    print(f"sync_aleph: {docs} -> content/product/, release notes -> {DATA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
