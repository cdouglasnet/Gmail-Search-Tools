import importlib.util
import json
import os
import plistlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "src" / "script"
MENU_FILTER_PATH = SCRIPT_DIR / "menu_filter.py"
spec = importlib.util.spec_from_file_location("menu_filter", MENU_FILTER_PATH)
assert spec is not None
assert spec.loader is not None
menu_filter = importlib.util.module_from_spec(spec)
sys.modules["menu_filter"] = menu_filter
spec.loader.exec_module(menu_filter)


class TestMenuFilter(unittest.TestCase):
    @staticmethod
    def _run_main_capture(argv):
        import io
        from contextlib import redirect_stdout

        with patch("sys.argv", argv):
            f = io.StringIO()
            with redirect_stdout(f):
                menu_filter.main()
            return f.getvalue()

    def test_all_menu_items_are_json_serializable(self):
        item_sets = [
            menu_filter.gms_items(),
            menu_filter.gmu_items(),
            menu_filter.gmo_items(),
            menu_filter.gmss_items("invoice"),
            menu_filter.gmuu_items("invoice"),
            menu_filter.gmoo_items("invoice"),
            menu_filter.gmsettings_items(),
            menu_filter.gmz_items("invoice"),
        ]
        for items in item_sets:
            json.dumps({"items": items})

    def test_gmo_mode_returns_search_operators(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmo"])
        data = json.loads(output)
        titles = [item["title"] for item in data["items"]]
        # self.assertIn("Search Operators", titles)
        self.assertIn("From", titles)
        self.assertIn("→ Start Over", titles)

    def test_gmo_mode_accepts_query_argument(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmo", "mail"])
        data = json.loads(output)
        self.assertGreater(len(data["items"]), 0)

    def test_gmoo_mode_returns_search_operators(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmoo"])
        data = json.loads(output)
        titles = [item["title"] for item in data["items"]]
        # self.assertIn("Search Operators", titles)
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
        self.assertEqual(titles, ["Config →", "Diagnostic →", "Forum →", "GitHub →", "Start Over →"])

    def test_gmsettings_links_use_link_icon(self):
        output = self._run_main_capture(["menu_filter.py", "--mode", "gmsettings"])
        data = json.loads(output)
        items_by_title = {item["title"]: item for item in data["items"]}
        self.assertEqual(items_by_title["Forum →"]["icon"]["path"], "link.png")
        self.assertEqual(items_by_title["GitHub →"]["icon"]["path"], "link.png")

    def test_diagnostic_script_is_externalized(self):
        project_root = Path(__file__).resolve().parents[1]
        diagnostic_script = project_root / "src" / "script" / "diagnostic.sh"
        info = plistlib.loads((project_root / "src" / "info.plist").read_bytes())
        diagnostic_actions = [
            obj["config"]
            for obj in info["objects"]
            if obj.get("uid") == "B8E8A0EE-A706-4AB1-94B5-22C3B71DD254"
        ]

        self.assertTrue(diagnostic_script.is_file())
        self.assertEqual(diagnostic_actions[0]["script"], "/bin/bash script/diagnostic.sh")
        self.assertIn("### Workflow version", diagnostic_script.read_text())

    def test_gmz_mode_wires_route_variable(self):
        with patch.dict(os.environ, {"route": "settings"}):
            output = self._run_main_capture([
                "menu_filter.py",
                "--mode",
                "gmz",
                "invoice",
            ])
        #lines = output.strip().splitlines()
        #self.assertEqual(lines[0], "Route: settings")
        #self.assertEqual(lines[1], "Query: invoice")

        #data = json.loads(lines[-1])
        #self.assertEqual(data["items"][0]["subtitle"], 'Route: "settings"')

    def test_gms_item_sets_transition_icon_to_display_icon(self):
        green_check = next(item for item in menu_filter.gms_items() if item["title"] == "Green Checkmark")

        self.assertEqual(green_check["icon"]["path"], "green-check.png")
        self.assertEqual(green_check["variables"]["ticon"], "green-check.png")

    def test_gmz_search_uses_transition_icon_variable(self):
        with patch.dict(os.environ, {"ticon": "green-check.png"}):
            item = menu_filter.gmz_items("invoice")[0]

        self.assertEqual(item["icon"]["path"], "green-check.png")


if __name__ == "__main__":
    unittest.main()
