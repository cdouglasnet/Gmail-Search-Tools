import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/script")))

import set_browser


class TestSetBrowser(unittest.TestCase):
    def test_parse_browser_rejects_empty(self):
        with self.assertRaises(Exception):
            set_browser.parse_browser("")
        with self.assertRaises(Exception):
            set_browser.parse_browser("   ")

    def test_parse_browser_accepts_valid_value(self):
        self.assertEqual(set_browser.parse_browser("Google Chrome"), "Google Chrome")

    def test_main_sets_target_browser(self):
        with patch("sys.argv", ["set_browser.py", "Safari"]):
            with patch("set_browser.set_alfred_workflow_variable") as mock_set_var:
                with patch("builtins.print") as mock_print:
                    with patch.dict(os.environ, {}, clear=True):
                        set_browser.main()

                        self.assertEqual(os.environ.get("target_browser"), "Safari")

        mock_set_var.assert_called_once_with("target_browser", "Safari", "net.cdoug.gmail-search-tools")
        mock_print.assert_called_once_with("target_browser=Safari")
