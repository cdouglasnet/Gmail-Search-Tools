import os
import sys
import unittest
from unittest.mock import patch

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
            with patch("builtins.print") as mock_print:
                set_user_number.main()

        self.assertEqual(os.environ.get("userNumber"), "3")
        mock_print.assert_called_once_with("userNumber=3")
