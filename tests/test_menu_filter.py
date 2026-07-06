import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/script")))

import menu_filter


class TestMenuFilter(unittest.TestCase):
    def _run_main_capture(self, argv):
        import io
        from contextlib import redirect_stdout

        with patch("sys.argv", argv):
            f = io.StringIO()
            with redirect_stdout(f):
                menu_filter.main()
            return f.getvalue()

    def test_gmo_mode_returns_search_operators(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmo"])
        data = json.loads(output)
        titles = [item["title"] for item in data["items"]]
        self.assertIn("Search Options", titles)
        self.assertIn("From", titles)
        self.assertIn("Start Over", titles)

    def test_gmo_mode_accepts_query_argument(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmo", "mail"])
        data = json.loads(output)
        self.assertGreater(len(data["items"]), 0)

    def test_gmoo_mode_returns_search_operators(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmoo"])
        data = json.loads(output)
        titles = [item["title"] for item in data["items"]]
        self.assertIn("Search Options", titles)
        self.assertIn("From:", titles)

    def test_gmoo_mode_wires_query_into_items(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmoo", "invoice"])
        data = json.loads(output)
        titles = [item["title"] for item in data["items"]]
        self.assertIn('From: "invoice"', titles)
        self.assertIn('Subject: "invoice"', titles)

    def test_gmsettings_mode_returns_expected_items(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmsettings"])
        data = json.loads(output)
        titles = [item["title"] for item in data["items"]]
        self.assertEqual(titles, ["Config", "Diagnostic", "Forum", "GitHub", "Start Over"])

    def test_gmsettings_links_use_link_icon(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmsettings"])
        data = json.loads(output)
        items_by_title = {item["title"]: item for item in data["items"]}
        self.assertEqual(items_by_title["Forum"]["icon"]["path"], "link.png")
        self.assertEqual(items_by_title["GitHub"]["icon"]["path"], "link.png")


if __name__ == "__main__":
    unittest.main()
