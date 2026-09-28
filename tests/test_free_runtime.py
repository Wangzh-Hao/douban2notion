from pathlib import Path
import os
import tempfile
import unittest
from unittest.mock import patch

from douban2notion.heatmap_utils import (
    build_heatmap_url,
    is_heatmap_embed_url,
    move_and_rename_file,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "douban2notion"
BLOCKED_HOSTS = (
    "wereadassets.malinkang.com",
    "i.malinkang.com",
    "notionhub.app",
    "heatmap.malinkang.com",
    "notion-icon.malinkang.com",
)


class FreeRuntimeTest(unittest.TestCase):
    def test_source_does_not_call_notionhub_services(self):
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SOURCE.rglob("*.py")
        )
        for host in BLOCKED_HOSTS:
            self.assertNotIn(host, source)

    def test_free_scope_is_movie_and_book(self):
        source = (SOURCE / "update_heatmap.py").read_text(encoding="utf-8")
        self.assertIn('{"movie", "book"}', source)

    def test_heatmap_embed_recognizes_all_supported_urls(self):
        urls = (
            "https://heatmap.malinkang.com/?image=old.svg",
            "https://raw.githubusercontent.com/o/r/main/.notionhub-artifacts/douban/book/1.svg",
            "https://raw.githubusercontent.com/o/r/heatmap-artifacts/OUT_FOLDER/book/2.svg",
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(is_heatmap_embed_url(url, "book"))
        self.assertFalse(
            is_heatmap_embed_url(
                "https://raw.githubusercontent.com/o/r/main/README.md", "book"
            )
        )

    def test_heatmap_artifact_defaults_to_published_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "OUT_FOLDER"
            output.mkdir()
            (output / "notion.svg").write_text("svg", encoding="utf-8")
            with patch.dict(
                os.environ, {"NOTIONHUB_ARTIFACT_ROOT": str(output)}, clear=True
            ), patch("time.time", return_value=123):
                previous = os.getcwd()
                try:
                    os.chdir(directory)
                    filename = move_and_rename_file("book")
                finally:
                    os.chdir(previous)
            self.assertEqual("123.svg", filename)
            self.assertTrue((output / "book" / filename).is_file())

    def test_heatmap_url_matches_workflow_publish_location(self):
        with patch.dict(os.environ, {}, clear=True):
            url = build_heatmap_url("owner/repo", "movie", "123.svg")
        self.assertEqual(
            "https://raw.githubusercontent.com/owner/repo/"
            "heatmap-artifacts/OUT_FOLDER/movie/123.svg",
            url,
        )


if __name__ == "__main__":
    unittest.main()
