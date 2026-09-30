import pathlib
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import check_site  # noqa: E402


def write(root: pathlib.Path, rel: str, body: str = "") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)


class CheckSiteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.public = pathlib.Path(self.tmp.name) / "public"
        self.legacy = pathlib.Path(self.tmp.name) / "legacy.tsv"
        self.legacy.write_text("# comment\nhttps://old.example/a\t/a/\n")
        patcher = mock.patch.object(check_site, "LEGACY", self.legacy)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_clean_site_passes(self):
        write(self.public, "a/index.html", '<a href="/b/">b</a><img src="img.png"><a href="https://x.y/">x</a>')
        write(self.public, "a/img.png")
        write(self.public, "b/index.html", '<a href="#top">top</a><a href="//cdn.example/x.js">cdn</a>')
        self.assertEqual(check_site.check(self.public), [])

    def test_missing_legacy_url_fails(self):
        write(self.public, "index.html")
        errors = check_site.check(self.public)
        self.assertEqual(len(errors), 1)
        self.assertIn("legacy URL https://old.example/a", errors[0])

    def test_broken_internal_link_fails(self):
        write(self.public, "a/index.html", '<a href="/missing/#x">m</a><link rel="stylesheet" href="/css/gone.css">')
        errors = check_site.check(self.public)
        self.assertEqual(
            errors,
            ["a/index.html: broken link /missing/#x", "a/index.html: broken link /css/gone.css"],
        )

    def test_percent_encoded_paths_resolve(self):
        write(self.public, "a/index.html", '<a href="/files/My%20Doc.pdf">pdf</a>')
        write(self.public, "files/My Doc.pdf")
        self.assertEqual(check_site.check(self.public), [])


if __name__ == "__main__":
    unittest.main()
