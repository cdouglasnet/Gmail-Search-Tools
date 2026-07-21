import os
import sys
import unittest
from unittest.mock import call, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/script")))

import set_user_number


class TestSetUserNumber(unittest.TestCase):
    def test_parse_account_accepts_0_to_9(self):
        self.assertEqual(set_user_number.parse_account("0"), "0")
        self.assertEqual(set_user_number.parse_account("9"), "9")

    def test_parse_account_rejects_non_integer(self):
        with self.assertRaises(Exception):
            set_user_number.parse_account("abc")

    def test_parse_account_rejects_out_of_range(self):
        with self.assertRaises(Exception):
            set_user_number.parse_account("-1")
        with self.assertRaises(Exception):
            set_user_number.parse_account("10")

    def test_main_sets_usernumber(self):
        with patch("sys.argv", ["set_user_number.py", "3"]):
            with patch("set_user_number.subprocess.run") as mock_run:
                with patch("builtins.print") as mock_print:
                    with patch.dict(os.environ, {}, clear=True):
                        set_user_number.main()

                        self.assertEqual(os.environ.get("userNumber"), "3")
                        self.assertEqual(os.environ.get("gmail_account"), "3")

        mock_run.assert_has_calls(
            [
                call(
                    [
                        "/usr/bin/osascript",
                        "-e",
                        (
                            'tell application id "com.runningwithcrayons.Alfred" '
                            'to set configuration "userNumber" to value "3" '
                            'in workflow "net.cdoug.gmail-search-tools"'
                        ),
                    ],
                    check=True,
                ),
                call(
                    [
                        "/usr/bin/osascript",
                        "-e",
                        (
                            'tell application id "com.runningwithcrayons.Alfred" '
                            'to set configuration "gmail_account" to value "3" '
                            'in workflow "net.cdoug.gmail-search-tools"'
                        ),
                    ],
                    check=True,
                ),
            ]
        )
        self.assertEqual(mock_run.call_count, 2)
        mock_print.assert_called_once_with("userNumber=3")
