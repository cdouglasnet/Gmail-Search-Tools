#!/usr/bin/env python3

import argparse
import json
import os
from urllib.parse import quote_plus

GMAIL_BASE_URL = "https://mail.google.com/mail/u/{account}/#search/{query}"
ICONS = {
    "gms-unread-menu": "unread.png",
    "gms-red-bang": "red-bang.png",
    "gms-yellow-bang": "yellow-bang.png",
    "gms-purple-question": "purple-question.png",
    "gms-blue-star": "blue-star.png",
    "gms-orange-guillemet": "orange-guillemet.png",
    "gms-yellow-star": "yellow-star.png",
    "gms-orange-star": "orange-star.png",
    "gms-red-star": "red-star.png",
    "gms-purple-star": "purple-star.png",
    "gms-green-star": "green-star.png",
    "gms-settings": "settings.png",
    "gmu-main": "unread.png",
    "gmu-search-unread": "unread.png",
    "gmu-settings": "settings.png",
    "gmu-back": "back.png",
}


def account_number():
    return os.environ.get("userNumber") or os.environ.get("gmail_account") or "0"


def gmail_url(query):
    return GMAIL_BASE_URL.format(account=account_number(), query=quote_plus(query))


def item(uid, title, subtitle, arg):
    result = {
        "uid": uid,
        "title": title,
        "subtitle": subtitle,
        "arg": arg,
        "valid": True,
    }
    icon_file = ICONS.get(uid)
    if icon_file:
        result["icon"] = {"path": icon_file}
    return result


def gms_items(query):
    q = query.strip()
    items = [
        item("gms-search-reference", "GMail Search Refrence", "Learn Power Searches", "search"),
        item("gms-unread-menu", "Un-Read Mail", "Unread quick links", "unread"),
        item(
            "gms-search",
            f'Search Gmail: "{q}"' if q else "Search Gmail",
            "Search all Gmail messages",
            gmail_url(q),
        ),
        item(
            "gms-search-unread",
            f'Search Unread: "{q}"' if q else "Search Unread",
            "Search unread Gmail messages",
            gmail_url(f"is:unread {q}".strip()),
        ),
        item("gms-red-bang", "Red Bang", "Show mail with red-bang star", gmail_url("has:red-bang")),
        item("gms-yellow-bang", "Yellow Bang", "Show mail with yellow-bang star", gmail_url("has:yellow-bang")),
        item("gms-purple-question", "Purple Question", "Show mail with purple-question star", gmail_url("has:purple-question")),
        item("gms-blue-info", "Blue Info", "Show mail with blue-info star", gmail_url("has:blue-info")),
        item("gms-blue-star", "Blue Star", "Show mail with blue-star", gmail_url("has:blue-star")),
        item("gms-orange-guillemet", "Orange Guillemet", "Show mail with orange-guillemet", gmail_url("has:orange-guillemet")),
        item("gms-yellow-star", "Yellow Star", "Show mail with yellow-star", gmail_url("has:yellow-star")),
        item("gms-orange-star", "Orange Star", "Show mail with orange-star", gmail_url("has:orange-star")),
        item("gms-red-star", "Red Star", "Show mail with red-star", gmail_url("has:red-star")),
        item("gms-purple-star", "Purple Star", "Show mail with purple-star", gmail_url("has:purple-star")),
        item("gms-green-star", "Green Star", "Show mail with green-star", gmail_url("has:green-star")),
        item("gms-green-check", "Green Checkmark", "Show mail with green-check", gmail_url("has:green-check")),
        item("gms-settings", "Settings", "Open workflow configuration", "settings"),
    ]
    return items


def gmu_items(query):
    q = query.strip()
    items = [
        item("gmu-main", "Un-Read Mail", "Unread quick links", "name"),
        item(
            "gmu-search-unread",
            f'Search Unread Gmail: "{q}"' if q else "Search Unread Gmail",
            "Search all unread Gmail messages",
            gmail_url(f"is:unread {q}".strip()),
        ),
        item("gmu-primary", "Primary Unread", "Unread in Primary", gmail_url("category:primary label:unread")),
        item("gmu-updates", "Updates UnRead", "Unread in Updates", gmail_url("category:updates label:unread")),
        item("gmu-promotions", "Promotions UnRead", "Unread in Promotions", gmail_url("category:promotions label:unread")),
        item("gmu-forums", "Forums UnRead", "Unread in Forums", gmail_url("category:forums label:unread")),
        item("gmu-reservations", "Reservations", "Reservations category", gmail_url("category:reservations")),
        item("gmu-purchases", "Purchases", "Purchases category", gmail_url("category:purchases")),
        item("gmu-settings", "Settings", "Open workflow configuration", "settings"),
        item("gmu-back", "Start Over", "Return to the main menu", "back"),
    ]
    return items


def main():
    parser = argparse.ArgumentParser(description="Gmail menu script filter")
    parser.add_argument("--mode", choices=["gms", "gmu"], required=True)
    parser.add_argument("query", nargs="*")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    items = gmu_items(query) if args.mode == "gmu" else gms_items(query)
    print(json.dumps({"items": items}, ensure_ascii=False))


if __name__ == "__main__":
    main()
