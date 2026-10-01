# Teramot Docs & Engineering

Teramot's documentation and engineering blog in one [Hugo](https://gohugo.io/)
site, built with the [Hextra](https://imfing.github.io/hextra/) theme and
deployed to [docs.teramot.com](https://docs.teramot.com) via GitHub Pages.

| Area | URL | Source |
| --- | --- | --- |
| Product | `/product/` | teramot-aleph `public-docs/`, synced (see below) |
| Architecture | `/architecture/` | `content/architecture/` |
| Compliance | `/compliance/` | `content/compliance/` |
| Product Updates | `/updates/` | `content/updates/` |
| Changelog | `/changelog/` | teramot-aleph release notes, synced (see below) |
| System Status | `/status/` | `content/status/` |
| Engineering Blog | `/blog/` | `content/blog/` |

Docs are available in English (`/`) and Spanish (`/es/`). The blog is English only.

## Local development

```sh
git clone --recurse-submodules git@github.com:HalleyScore/teramot-docs.git
cd teramot-docs
hugo server
```

The site is served at http://localhost:1313/.

`/product/` and `/changelog/` are empty until you sync them from a teramot-aleph
checkout next to this repo (`--aleph <path>` for another location):

```sh
python3 scripts/sync_aleph.py
```

## Product docs and changelog (from teramot-aleph)

The pages under `/product/` are written in teramot-aleph's `public-docs/`, where CI
checks each one against the code; the changelog is the release notes its release cut
writes (`frontend/public/release-notes.json`), in English and Spanish.
`scripts/sync_aleph.py` copies both in before every build, into gitignored paths
(`content/product/`, `static/product/`, `data/aleph/`): never edit them here, and
fix a page in aleph instead.

The sync adapts aleph's Markdown to this site: relative links become `/product/...`
URLs, a `tabs` block becomes Hextra tabs (one per heading, with an anchor so a link
to the heading opens its tab; `assets/js/product-tabs.js`), a `cards` block becomes
`{{< link-cards >}}`, and a paragraph opening with **Where:** becomes a quote. Each
aleph folder gets its sidebar title from `SECTIONS`; a new folder still publishes,
titled after its directory, and the run shows a warning to add it.

Every aleph page has its Spanish translation next to it (`page.es.md`), checked in
aleph like the English one; the sync publishes it at `/es/product/...`.

The MCP pages (`/product/mcp/`) replaced the hand-written `/api/` section: `ALIASES` in
the sync keeps each old `/api/...` URL, in both languages, redirecting to its page.

CI publishes aleph's latest `vX.Y.Z` tag, which is what prd runs. aleph's Build &
Deploy dispatches `hugo.yml` with the tag after each prd rollout, and a manual run
(Actions → Run workflow) takes any ref in `aleph_ref`. aleph is private, so CI reads
it with the `ALEPH_READ_TOKEN` secret (a fine-grained token with Contents: Read-only
on teramot-aleph); without it the build fails rather than publish a site with no
product docs.

### Prerequisites

Hugo **extended** (CI pins the version in `.github/workflows/hugo.yml`), plus
`asciidoctor` and `rouge`, which Hugo shells out to for `.adoc` content. They are
not optional if any page uses AsciiDoc: a missing binary fails the build.

```sh
sudo pacman -S hugo asciidoctor ruby-rouge      # Arch
sudo apt install hugo asciidoctor ruby-rouge    # Debian/Ubuntu
```

Python 3 runs the site checks (no packages needed).

## Writing docs

A docs page is a Markdown file in its section. The path is the URL:
`content/architecture/my-page.md` is published at `/architecture/my-page/`.

```sh
hugo new content architecture/my-page.md
```

- **Order and sidebar label:** `weight` (lower first) and `linkTitle` in the
  front matter. Each top-level section has its own sidebar.
- **Spanish:** add `my-page.es.md` next to it, with the same `weight`. Internal
  links in Spanish pages point at `/es/...`. A page without a translation is
  simply missing from the Spanish site, so translate new docs in the same PR.
- **Components:** GitHub-style alerts (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`),
  ```` ```mermaid ```` diagrams, and Hextra shortcodes such as
  [tabs](https://imfing.github.io/hextra/docs/guide/shortcodes/tabs/) and
  [cards](https://imfing.github.io/hextra/docs/guide/shortcodes/cards/).
- **Images and downloads:** under `static/img/` and `static/files/`, linked from
  the site root (`/img/...`), or next to the page in a page bundle.
- **Never rename or move a published page** without keeping its old URL: add
  the old path to `aliases:` in the front matter. `scripts/legacy-urls.tsv`
  lists every URL published before the sites merged, and CI fails if one stops
  resolving.

## Writing a blog post

```sh
hugo new content blog/my-post-slug/index.md    # Markdown
hugo new content blog/my-post-slug/index.adoc  # AsciiDoc
```

Edit the front matter, then set `draft: false` to publish.

- **Authors** are slugs: `authors: [facundo-vivas]`. A new author needs
  `data/authors/<slug>.json` (name, bio, image, links) and
  `content/authors/<slug>/_index.md` (profile page at `/blog/authors/<slug>/`).
  Author photos go in `assets/images/authors/`.
- **Card image:** put `feature.png` (or `.jpg`/`.webp`) in the post folder. Without
  one, the card shows a Teramot panel for the post's first `categories` entry.
- **Date:** posts are ordered by `date`. When two posts share a day, give them a
  time (`2026-09-11T16:50:39-03:00`).
- **Shortcodes** for posts: `intro`, `inlinesvg`, `stats`/`stat`, `chart`
  (Chart.js config) and `timeline`/`timelineItem`, in `layouts/_shortcodes/`.
- View counts come from GoatCounter (cookieless) on blog pages only; see
  `config/_default/params.toml`.

### AsciiDoc notes

Rendering is configured in `config/_default/markup.toml` (`[asciidocExt]`), and
`asciidoctor` is allowed to run in `config/_default/security.toml`. Hugo refuses
to exec binaries that are not on that allowlist, and the list replaces Hugo's
defaults rather than extending them, so keep it in sync when Hugo is upgraded.

- Front matter is still Hugo's (`---` YAML), not an AsciiDoc document header.
  Do not add a `= Title` line; the `title` key already renders one.
- Heading IDs match Goldmark's (`#my-heading`), so anchors behave the same.
- Shortcodes work. Asciidoctor wraps a block-level shortcode in its own
  `<div class="paragraph">`; wrap the call in a `++++` passthrough block to
  avoid the stray margin.
- Code blocks are highlighted by Rouge instead of Chroma, coloured by a
  generated block in `assets/css/custom.css`. After upgrading the Hextra
  submodule, re-run `python3 scripts/gen-rouge-css.py`.

## Checks

```sh
python3 scripts/sync_aleph.py
hugo --gc --minify
python3 -m unittest discover -s scripts/tests
python3 scripts/check_site.py public
```

`check_site.py` fails if any URL in `scripts/legacy-urls.tsv` no longer
resolves, or if any page links to a file that does not exist. CI runs all three
on every pull request.

## Layout of the repo

| Path | Purpose |
| --- | --- |
| `content/` | Docs, blog posts and landing pages (Markdown/AsciiDoc) |
| `config/_default/` | Site config, menus (`menus.<lang>.toml`), theme params |
| `layouts/` | Overrides of the theme: home, blog cards, post meta, shortcodes |
| `assets/` | CSS (branding), JS, SVGs and author photos processed by Hugo |
| `static/` | Files served as-is: images, PDFs, icons, `CNAME` |
| `i18n/` | UI strings per language |
| `themes/hextra/` | Theme, pinned as a git submodule |
| `scripts/` | Site checks, the teramot-aleph sync, favicon and Rouge CSS generators |

Keep theme changes in `layouts/` and `assets/`; never edit the submodule. The
files copied from Hextra (`layouts/blog/single.html`, `layouts/authors/term.html`)
say so in their first line: re-sync them when upgrading the theme.

## Icons and link previews

The Teramot icon set in `static/` shadows the theme's own (project `static/`
wins at the same path) and is generated from `static/brand/teramot-favicon.svg`:

```sh
./scripts/gen-favicons.sh    # needs rsvg-convert and ImageMagick 7
```

`layouts/_partials/favicons.html` declares the whole set. Bump the `$v`
cache-buster in it when the mark changes.

## Deploy

Pushing to `main` runs `.github/workflows/hugo.yml`, which builds the site,
runs the checks and publishes it via GitHub Pages. Pull requests build and
check only.

The site is always built for `https://docs.teramot.com/`: docs link to root
paths, so it only works served from a domain root.

## DNS and custom domain

`docs.teramot.com` needs a `CNAME` record pointing at `halleyscore.github.io`.
DNS is not managed in this repo.

With Actions-based Pages deploys, GitHub does **not** pick the custom domain up
from `static/CNAME`; register it on the repo once:

```sh
gh api -X PUT repos/HalleyScore/teramot-docs/pages -f "cname=docs.teramot.com"
gh api -X PUT repos/HalleyScore/teramot-docs/pages -F "https_enforced=true"
```
