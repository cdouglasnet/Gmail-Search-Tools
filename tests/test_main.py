# tests/test_main.py
import json
import os
import sys
import unittest
from unittest.mock import patch

# Add src directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/script')))

import main


class TestGmailUrlBuilder(unittest.TestCase):
    def test_build_gmail_url_no_prefix(self):
        url = main.build_gmail_url("hello world")
        self.assertIn("mail.google.com", url)
        self.assertIn("hello+world", url)

    def test_build_gmail_url_with_prefix(self):
        url = main.build_gmail_url("hello", "is:unread")
        self.assertIn("is%3Aunread", url)
        self.assertIn("hello", url)

    def test_build_gmail_url_empty_query(self):
        url = main.build_gmail_url("")
        self.assertIn("mail.google.com", url)

    def test_build_gmail_url_default_account(self):
        url = main.build_gmail_url("test")
        self.assertIn("/u/0/", url)

    def test_build_gmail_url_custom_account(self):
        with patch.dict(os.environ, {"gmail_account": "1"}):
            url = main.build_gmail_url("test")
        self.assertIn("/u/1/", url)


class TestBuildSearchItems(unittest.TestCase):
    def test_general_search_returns_items(self):
        items = main.build_search_items("test query")
        self.assertGreater(len(items), 0)

    def test_general_search_includes_unread_option(self):
        items = main.build_search_items("test")
        titles = [item["title"] for item in items]
        self.assertTrue(any("Unread" in t for t in titles))

    def test_general_search_first_item_is_all_gmail(self):
        items = main.build_search_items("test")
        self.assertIn("Search Gmail", items[0]["title"])

    def test_general_search_items_have_required_keys(self):
        items = main.build_search_items("test")
        required_keys = {"uid", "title", "subtitle", "arg", "valid"}
        for item in items:
            self.assertTrue(required_keys.issubset(item.keys()),
                            f"Item missing keys: {required_keys - item.keys()}")

    def test_general_search_items_are_valid(self):
        items = main.build_search_items("test")
        for item in items:
            self.assertTrue(item["valid"])

    def test_general_search_items_have_gmail_urls(self):
        items = main.build_search_items("test")
        for item in items:
            self.assertIn("mail.google.com", item["arg"])

    def test_general_search_query_in_title(self):
        items = main.build_search_items("my query")
        for item in items:
            self.assertIn("my query", item["title"])

    def test_general_search_empty_query(self):
        items = main.build_search_items("")
        self.assertGreater(len(items), 0)
        # No query means just the label, no quoted query
        for item in items:
            self.assertNotIn('""', item["title"])

    def test_unread_mode_returns_items(self):
        items = main.build_search_items("test", unread_mode=True)
        self.assertGreater(len(items), 0)

    def test_unread_mode_all_items_contain_unread(self):
        items = main.build_search_items("test", unread_mode=True)
        for item in items:
            self.assertIn("Unread", item["title"])

    def test_unread_mode_urls_contain_unread_filter(self):
        items = main.build_search_items("test", unread_mode=True)
        for item in items:
            self.assertIn("is%3Aunread", item["arg"])

    def test_unread_mode_query_in_title(self):
        items = main.build_search_items("my query", unread_mode=True)
        for item in items:
            self.assertIn("my query", item["title"])

    def test_general_search_different_from_unread_mode(self):
        general = main.build_search_items("test", unread_mode=False)
        unread = main.build_search_items("test", unread_mode=True)
        # Unread mode should have fewer / different items
        self.assertNotEqual(
            [i["title"] for i in general],
            [i["title"] for i in unread]
        )


class TestMainOutput(unittest.TestCase):
    def _run_main_capture(self, argv):
        """Run main() with given argv and capture stdout output."""
        import io
        from contextlib import redirect_stdout

        with patch('sys.argv', argv):
            f = io.StringIO()
            with redirect_stdout(f):
                try:
                    main.main()
                except SystemExit:
                    pass
            return f.getvalue()

    def test_main_returns_valid_json(self):
        output = self._run_main_capture(['main.py', 'test query'])
        data = json.loads(output)
        self.assertIn("items", data)

    def test_main_unread_mode_returns_valid_json(self):
        output = self._run_main_capture(['main.py', '--unread', 'test'])
        data = json.loads(output)
        self.assertIn("items", data)

    def test_main_empty_query_returns_items(self):
        output = self._run_main_capture(['main.py'])
        data = json.loads(output)
        self.assertGreater(len(data["items"]), 0)

    def test_main_unread_empty_query_returns_items(self):
        output = self._run_main_capture(['main.py', '--unread'])
        data = json.loads(output)
        self.assertGreater(len(data["items"]), 0)


if __name__ == '__main__':
    unittest.main()
