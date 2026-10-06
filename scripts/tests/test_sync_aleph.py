import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import sync_aleph  # noqa: E402


def write(root: pathlib.Path, rel: str, body: str = "") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)


PAGE = """---
title: Connect your data
description: How to connect a source.
sidebar_position: 2
covers:
  - frontend/src/**
---

# Connect your data

**Where:** **Sources** in the sidebar →
**New source**.

See [databases](./databases.md#snowflake) and [roles](../concepts/roles.md).

[//]: # (cards:start)

- [![](./logos/pg.svg) PostgreSQL](./databases.md)

[//]: # (cards:end)

[//]: # (tabs:start)

## Claude Desktop

Open **Settings**.

### Details

More.

## ChatGPT

Open **Apps**.

[//]: # (tabs:end)

```
[//]: # (tabs:start)
```
"""


class SyncAlephTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = pathlib.Path(tmp.name)
        self.aleph = root / "aleph"
        for name, value in {
            "CONTENT": root / "site/content/product",
            "STATIC": root / "site/static/product",
            "DATA": root / "site/data/aleph/release_notes.json",
        }.items():
            patcher = mock.patch.object(sync_aleph, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        write(self.aleph, "public-docs/index.md", "---\ntitle: Teramot documentation\n---\n\n# Teramot\n\nHi.\n")
        write(self.aleph, "public-docs/connect-data/overview.md", PAGE)
        write(self.aleph, "public-docs/connect-data/logos/pg.svg", "<svg/>")
        write(self.aleph, "public-docs/.forbidden-terms", "gold\n")
        write(self.aleph, "public-docs/embed.go", "package publicdocs\n")

    def synced(self, rel: str) -> str:
        sync_aleph.sync_docs(self.aleph / "public-docs")
        return (sync_aleph.CONTENT / rel).read_text()

    def test_front_matter_keeps_only_what_hugo_reads(self):
        out = self.synced("connect-data/overview.md")
        self.assertTrue(out.startswith('---\ntitle: "Connect your data"\ndescription: "How to connect a source."\nweight: 2\n---\n'))
        self.assertNotIn("covers", out)
        self.assertNotIn("# Connect your data", out)

    def test_links_become_site_urls(self):
        out = self.synced("connect-data/overview.md")
        self.assertIn("[databases](/product/connect-data/databases/#snowflake)", out)
        self.assertIn("[roles](/product/concepts/roles/)", out)
        self.assertIn("![](/product/connect-data/logos/pg.svg)", out)
        self.assertTrue((sync_aleph.STATIC / "connect-data/logos/pg.svg").exists())

    def test_blocks_become_shortcodes(self):
        out = self.synced("connect-data/overview.md")
        self.assertIn("{{< link-cards >}}\n\n- [![](/product/connect-data/logos/pg.svg) PostgreSQL]", out)
        self.assertIn('{{< tab name="Claude Desktop" >}}\n<span id="claude-desktop" class="tm-tab-anchor"></span>', out)
        self.assertIn("### Details", out)
        self.assertEqual(out.count("{{< tab "), 2)
        self.assertNotIn("[//]: # (tabs", out.split("```")[0])
        # A marker inside a code block is text, not a block.
        self.assertIn("```\n[//]: # (tabs:start)\n```", out)

    def test_where_paragraph_is_a_quote(self):
        out = self.synced("connect-data/overview.md")
        self.assertIn("> **Where:** **Sources** in the sidebar →\n> **New source**.\n\nSee", out)

    def test_index_is_the_section_root_and_folders_get_titles(self):
        root = self.synced("_index.md")
        self.assertIn("cascade:\n  type: docs\n", root)
        section = (sync_aleph.CONTENT / "connect-data/_index.md").read_text()
        self.assertEqual(section, '---\ntitle: "Connect your data"\nweight: 20\nlayout: first-page\n---\n')

    def test_a_retired_url_redirects_to_its_page(self):
        write(self.aleph, "public-docs/mcp/overview.md", "---\ntitle: Overview\n---\n")
        out = self.synced("mcp/overview.md")
        self.assertIn('aliases: ["/api/intro/"]', out)
        self.assertIn('aliases: ["/api/"]', (sync_aleph.CONTENT / "mcp/_index.md").read_text())

    def test_a_translation_is_published_under_es(self):
        write(self.aleph, "public-docs/index.es.md", "---\ntitle: Documentación\ntranslation_of: abc\n---\n\nHola.\n")
        write(self.aleph, "public-docs/connect-data/overview.es.md",
              "---\ntitle: Conectá tus datos\ntranslation_of: abc\n---\n\n"
              "**Dónde:** **Fuentes**.\n\nVer [bases](./databases.es.md#cómo-conectar).\n")
        out = self.synced("connect-data/overview.es.md")
        self.assertNotIn("translation_of", out)
        self.assertIn("> **Dónde:** **Fuentes**.", out)
        self.assertIn("[bases](/es/product/connect-data/databases/#cómo-conectar)", out)
        self.assertIn("cascade:", (sync_aleph.CONTENT / "_index.es.md").read_text())
        self.assertEqual((sync_aleph.CONTENT / "connect-data/_index.es.md").read_text(),
                         '---\ntitle: "Conectar tus datos"\nweight: 20\nlayout: first-page\n---\n')

    def test_slugs_keep_accents(self):
        self.assertEqual(sync_aleph.slug("Cómo llega Teramot"), "cómo-llega-teramot")

    def test_only_pages_and_images_are_copied(self):
        sync_aleph.sync_docs(self.aleph / "public-docs")
        self.assertFalse((sync_aleph.CONTENT / "embed.go").exists())
        self.assertFalse(any(p.name.startswith(".") for p in sync_aleph.CONTENT.rglob("*")))

    def test_a_folder_without_a_title_still_publishes(self):
        write(self.aleph, "public-docs/data-billing/plans.md", "---\ntitle: Plans\n---\n")
        with mock.patch("sys.stderr") as stderr:
            sync_aleph.sync_docs(self.aleph / "public-docs")
        section = (sync_aleph.CONTENT / "data-billing/_index.md").read_text()
        self.assertEqual(section, '---\ntitle: "Data billing"\nweight: 100\nlayout: first-page\n---\n')
        self.assertIn("::warning::", "".join(c.args[0] for c in stderr.write.call_args_list))

    def test_release_notes_are_copied(self):
        notes = self.aleph / "release-notes.json"
        notes.write_text(json.dumps({"releases": [{"version": "v1.0.0", "date": "2026-09-01", "notes": []}]}))
        sync_aleph.sync_release_notes(notes)
        self.assertEqual(json.loads(sync_aleph.DATA.read_text())["releases"][0]["version"], "v1.0.0")


if __name__ == "__main__":
    unittest.main()
