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


if __name__ == "__main__":
    unittest.main()
