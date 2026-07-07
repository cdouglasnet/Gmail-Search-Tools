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

    def test_item_includes_settings_modifier(self):
        data = menu_filter.item("test-item", "Title", "Subtitle", "unread")
        self.assertEqual(
            data["mods"]["alt+shift"],
            {
                "valid": True,
                "arg": "settings",
                "subtitle": "Open Settings",
            },
        )

    def test_item_omits_modifiers_when_invalid(self):
        data = menu_filter.item("test-item", "Title", "Subtitle", valid=False)
        self.assertNotIn("mods", data)

    def test_mod_builds_cmd_modifier_with_default_modifiers(self):
        data = menu_filter.mod("cmd", "Custom Arg", "Custom Subtitle")
        self.assertEqual(
            data["cmd"],
            {
                "valid": True,
                "arg": "Custom Arg",
                "subtitle": "Custom Subtitle",
            },
        )
        self.assertEqual(data["alt+shift"]["arg"], "settings")

    def test_mod_uses_passed_modifier_key(self):
        data = menu_filter.mod("alt", "Custom Arg", "Custom Subtitle")
        self.assertEqual(
            data["alt"],
            {
                "valid": True,
                "arg": "Custom Arg",
                "subtitle": "Custom Subtitle",
            },
        )

    def test_main_menu_items_include_settings_modifier(self):
        for item in (
            menu_filter.gms_items("")[0],
            menu_filter.gmu_items("")[0],
            menu_filter.gmo_items()[0],
        ):
            self.assertEqual(item["mods"]["alt+shift"]["arg"], "settings")

    def test_all_menu_items_are_json_serializable(self):
        item_sets = [
            menu_filter.gms_items(""),
            menu_filter.gmss_items("invoice"),
            menu_filter.gmu_items(""),
            menu_filter.gmuu_items("invoice"),
            menu_filter.gmo_items(),
            menu_filter.gmoo_items("invoice"),
            menu_filter.gmsettings_items(),
            menu_filter.gmz_items("invoice"),
        ]
        for items in item_sets:
            json.dumps({"items": items})

    def test_gms_search_item_cmd_modifier_is_json_object(self):
        search_item = menu_filter.gms_items("")[1]
        self.assertEqual(
            search_item["mods"]["cmd"],
            {
                "valid": True,
                "arg": "CMD Pressed Arg",
                "subtitle": "CMD Pressed Subtitle",
            },
        )

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


if __name__ == "__main__":
    unittest.main()
