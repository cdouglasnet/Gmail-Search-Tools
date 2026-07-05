#!/usr/bin/env python3

import argparse
import json
import os
from urllib.parse import quote_plus

GMAIL_BASE_URL = "https://mail.google.com/mail/u/{account}/#search/{query}"
STATIC_ICONS = {
    "gms-unread-menu": "unread.png",
    "gms-red-bang": "red-bang.png",
    "gms-yellow-bang": "yellow-bang.png",
    "gms-purple-question": "purple-question.png",
    "gms-blue-info": "blue-info.png",
    "gms-blue-star": "blue-star.png",
    "gms-orange-guillemet": "orange-guillemet.png",
    "gms-yellow-star": "yellow-star.png",
    "gms-orange-star": "orange-star.png",
    "gms-red-star": "red-star.png",
    "gms-purple-star": "purple-star.png",
    "gms-green-check": "green-check.png",
    "gms-green-star": "green-star.png",
    "gms-settings": "settings.png",
    "gmu-main": "unread.png",
    "gmu-search-unread": "unread.png",
    "gmu-settings": "settings.png",
    "gmu-back": "back.png",
    "gmo-back": "back.png",
    "gmsettings-config": "settings.png",
    "gmsettings-diagnostic": "settings.png",
    "gmsettings-forum": "link.png",
    "gmsettings-github": "link.png",
    "gmsettings-back": "back.png",
}

# Currency icon mapping
CURRENCY_ICONS = {
    "dollar": "green-dollar.png",
    "pound": "green-pound.png",
    "euro": "green-euro.png",
    "yen": "green-yen.png",
}


def get_currency_icon():
    """Get the current currency icon based on environment variable"""
    currency = os.environ.get("currency", "dollar")
    return CURRENCY_ICONS.get(currency, CURRENCY_ICONS["dollar"])


def get_icon_for_uid(uid):
    """Get icon file for a uid, including currency-based icons"""
    if uid in STATIC_ICONS:
        return STATIC_ICONS[uid]
    if uid in ("gmu-promotions", "gmu-reservations", "gmu-purchases"):
        return get_currency_icon()
    return None

# Gmail can have multiple accounts logged in at a time. The account number is used to differentiate the accounts.
def account_number():
    return os.environ.get("userNumber") or os.environ.get("gmail_account") or "0"


def gmail_url(query):
    return GMAIL_BASE_URL.format(account=account_number(), query=quote_plus(query))


def item(uid, title, subtitle, arg=None, valid=True):
    result = {
        "title": title,
        "subtitle": subtitle,
        "valid": valid,
    }
    if arg is not None:
        result["arg"] = arg
    icon_file = get_icon_for_uid(uid)
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
        item(
            "gms-yellow-bang",
            "Yellow Bang",
            "Show mail with yellow-bang star",
            gmail_url("has:yellow-bang"),
        ),
        item(
            "gms-purple-question",
            "Purple Question",
            "Show mail with purple-question star",
            gmail_url("has:purple-question"),
        ),
        item(
            "gms-blue-info",
            "Blue Info",
            "Show mail with blue-info star",
            gmail_url("has:blue-info"),
        ),
        item("gms-blue-star", "Blue Star", "Show mail with blue-star", gmail_url("has:blue-star")),
        item(
            "gms-orange-guillemet",
            "Orange Guillemet",
            "Show mail with orange-guillemet",
            gmail_url("has:orange-guillemet"),
        ),
        item("gms-yellow-star", "Yellow Star", "Show mail with yellow-star", gmail_url("has:yellow-star")),
        item("gms-orange-star", "Orange Star", "Show mail with orange-star", gmail_url("has:orange-star")),
        item("gms-red-star", "Red Star", "Show mail with red-star", gmail_url("has:red-star")),
        item("gms-purple-star", "Purple Star", "Show mail with purple-star", gmail_url("has:purple-star")),
        item("gms-green-star", "Green Star", "Show mail with green-star", gmail_url("has:green-star")),
        item(
            "gms-green-check",
            "Green Checkmark",
            "Show mail with green-check",
            gmail_url("has:green-check"),
        ),
        item("gms-settings", "Settings", "Open workflow configuration", "settings"),
    ]
    return items

def gmss_items(query):
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
        item(
            "gms-yellow-bang",
            "Yellow Bang",
            "Show mail with yellow-bang star",
            gmail_url("has:yellow-bang"),
        ),
        item(
            "gms-purple-question",
            "Purple Question",
            "Show mail with purple-question star",
            gmail_url("has:purple-question"),
        ),
        item(
            "gms-blue-info",
            "Blue Info",
            "Show mail with blue-info star",
            gmail_url("has:blue-info"),
        ),
        item("gms-blue-star", "Blue Star", "Show mail with blue-star", gmail_url("has:blue-star")),
        item(
            "gms-orange-guillemet",
            "Orange Guillemet",
            "Show mail with orange-guillemet",
            gmail_url("has:orange-guillemet"),
        ),
        item("gms-yellow-star", "Yellow Star", "Show mail with yellow-star", gmail_url("has:yellow-star")),
        item("gms-orange-star", "Orange Star", "Show mail with orange-star", gmail_url("has:orange-star")),
        item("gms-red-star", "Red Star", "Show mail with red-star", gmail_url("has:red-star")),
        item("gms-purple-star", "Purple Star", "Show mail with purple-star", gmail_url("has:purple-star")),
        item("gms-green-star", "Green Star", "Show mail with green-star", gmail_url("has:green-star")),
        item(
            "gms-green-check",
            "Green Checkmark",
            "Show mail with green-check",
            gmail_url("has:green-check"),
        ),
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
        item(
            "gmu-primary",
            "Primary Unread",
            "Unread in Primary",
            gmail_url("category:primary label:unread"),
        ),
        item(
            "gmu-updates",
            "Updates UnRead",
            "Unread in Updates",
            gmail_url("category:updates label:unread"),
        ),
        item(
            "gmu-promotions",
            "Promotions UnRead",
            "Unread in Promotions",
            gmail_url("category:promotions label:unread"),
        ),
        item(
            "gmu-forums",
            "Forums UnRead",
            "Unread in Forums",
            gmail_url("category:forums label:unread"),
        ),
        item(
            "gmu-reservations",
            "Reservations",
            "Reservations category",
            gmail_url("category:reservations"),
        ),
        item("gmu-purchases", "Purchases", "Purchases category", gmail_url("category:purchases")),
        item("gmu-settings", "Settings", "Open workflow configuration", "settings"),
        item("gmu-back", "Start Over", "Return to the main menu", "back"),
    ]
    return items

def gmuu_items(query):
    q = query.strip()
    items = [
        item("gmu-main", "Un-Read Mail", "Unread quick links", "name"),
        item(
            "gmu-search-unread",
            f'Search Unread Gmail: "{q}"' if q else "Search Unread Gmail",
            "Search all unread Gmail messages",
            gmail_url(f"is:unread {q}".strip()),
        ),
        item(
            "gmu-primary",
            "Primary Unread",
            "Unread in Primary",
            gmail_url("category:primary label:unread"),
        ),
        item(
            "gmu-updates",
            "Updates UnRead",
            "Unread in Updates",
            gmail_url("category:updates label:unread"),
        ),
        item(
            "gmu-promotions",
            "Promotions UnRead",
            "Unread in Promotions",
            gmail_url("category:promotions label:unread"),
        ),
        item(
            "gmu-forums",
            "Forums UnRead",
            "Unread in Forums",
            gmail_url("category:forums label:unread"),
        ),
        item(
            "gmu-reservations",
            "Reservations",
            "Reservations category",
            gmail_url("category:reservations"),
        ),
        item("gmu-purchases", "Purchases", "Purchases category", gmail_url("category:purchases")),
        item("gmu-settings", "Settings", "Open workflow configuration", "settings"),
        item("gmu-back", "Start Over", "Return to the main menu", "back"),
    ]
    return items


def gmo_items():
    items = [
        item(
            "gmo-search-options",
            "Search Options",
            "↵ Copy, ⌘ Auto, ⌥ Auto Clip, ⌃ Other, ⇧⌘ Back",
            valid=False,
        ),
        item("gmo-from", "From", "Ex. from:bob", "from:"),
        item("gmo-to", "To", "Ex. to:bob", "to:"),
        item("gmo-cc", "CC", "Ex. cc:bob", "cc:"),
        item("gmo-bcc", "BCC", "Ex. bcc:bob", "bcc:"),
        item("gmo-subject", "Subject", "Ex. subject:what about bob", "subject:"),
        item("gmo-or", "OR", "Ex. from:bob OR from:bam", "OR"),
        item("gmo-exclude", "Exclude", "Ex. bam -rock", "-"),
        item("gmo-around", "AROUND", "Ex. flight AROUND 10 airport", "AROUND"),
        item("gmo-label", "Label", "Ex. label:builders", "label:"),
        item("gmo-attachments", "Attachments", "Ex. has:attachment", "has:attachment"),
        item("gmo-drive-link", "Drive Link", "Ex. has:drive", "has:drive"),
        item("gmo-document", "Document", "Ex. has:document", "has:document"),
        item("gmo-spreadsheet", "Spreadsheet", "Ex. has:spreadsheet", "has:spreadsheet"),
        item("gmo-presentation", "Presentation", "Ex. has:presentation", "has:presentation"),
        item("gmo-youtube", "YouTube", "Ex. has:youtube", "has:youtube"),
        item("gmo-list", "List", "Ex. list:info@example.org", "list:"),
        item("gmo-filename", "Filename", "Ex. filename:wishlist.txt", "filename:"),
        item(
            "gmo-exact-word-or-phrase",
            "Exact Word or Phrase",
            'Ex. "bob the builder"',
            '""',
        ),
        item("gmo-group-search-terms", "Group Search Terms", "Ex. (bob builder)", "()"),
        item(
            "gmo-anywhere",
            "Anywhere (include Spam & Trash)",
            "Ex. in:anywhere",
            "in:anywhere",
        ),
        item("gmo-important", "Important", "Ex. is:important", "is:important"),
        item("gmo-after", "After", "Ex. after:08/28/2024", "after:"),
        item("gmo-before", "Before", "Ex. before:08/28/2004", "before:"),
        item("gmo-older", "Older", "Ex. older:08/28/2004", "older:"),
        item("gmo-newer", "Newer", "Ex. newer:08/28/2004", "newer:"),
        item(
            "gmo-older-than",
            "Older Than (d=Day m=Mnth y=Yr)",
            "Ex. older_than:2d",
            "older_than:",
        ),
        item("gmo-chat", "Chat", "Ex. is:chat", "is:chat"),
        item(
            "gmo-delivered-to",
            "Delivered To",
            "Ex. deliveredto:username@gmail.com",
            "deliveredto:@gmail.com",
        ),
        item("gmo-primary-category", "Primary Category", "Ex. category:primary", "category:primary"),
        item("gmo-social-category", "Social Category", "Ex. category:social", "category:social"),
        item(
            "gmo-promotions-category",
            "Promotions Category",
            "Ex. category:promotions",
            "category:promotions",
        ),
        item("gmo-updates-category", "Updates Category", "Ex. category:updates", "category:updates"),
        item("gmo-forums-category", "Forums Category", "category:forums", "category:forums"),
        item(
            "gmo-reservations-category",
            "Reservations Category",
            "Ex. category:reservations",
            "category:reservations",
        ),
        item(
            "gmo-purchases-category",
            "Purchases Category",
            "Ex. category:purchases",
            "category:purchases",
        ),
        item("gmo-size-larger", "Size (Larger)", "Ex. size:1000000 (bytes / K / M)", "size:"),
        item("gmo-larger-size", "Larger Size", "Ex. larger:10M", "larger:"),
        item("gmo-smaller-size", "Smaller Size", "Ex. smaller:1M", "smaller:"),
        item("gmo-exact-word-match", "Exact Word Match", "Ex. +unicorn", "+"),
        item(
            "gmo-user-label",
            "User Label (Has Any User Label)",
            "Ex. has:userlabels",
            "has:userlabels",
        ),
        item("gmo-no-user-labels", "No User Labels", "Ex. has:nouserlabels", "has:nouserlabels"),
        item("gmo-unread", "Un-Read", "", "unread"),
        item("gmo-back", "Start Over", "Return to the main menu", "back"),
    ]
    return items


def gmsettings_items():
    return [
        item(
            "gmsettings-config",
            "Config",
            "Open workflow configuration in Alfred",
            "config",
        ),
        item(
            "gmsettings-diagnostic",
            "Diagnostic",
            "Run workflow diagnostic",
            "diagnostic",
        ),
        item(
            "gmsettings-forum",
            "Forum",
            "Open Alfred Forum page",
            "forum",
        ),
        item(
            "gmsettings-github",
            "GitHub",
            "Open GitHub project page",
            "github",
        ),
        item("gmsettings-back", "Start Over", "Return to the main menu", "back"),
    ]


def main():
    parser = argparse.ArgumentParser(description="Gmail menu script filter")
    parser.add_argument(
        "--mode",
        choices=["gms", "gmss", "gmu", "gmuu", "gmo", "gmsettings"],
        required=True,
    )
    parser.add_argument("query", nargs="*")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if args.mode == "gmu":
        items = gmu_items(query)
    elif args.mode == "gmuu":
        items = gmuu_items(query)
    elif args.mode == "gmss":
        items = gmss_items(query)
    elif args.mode == "gmo":
        items = gmo_items()
    elif args.mode == "gmsettings":
        items = gmsettings_items()
    else:
        items = gms_items(query)
    print(json.dumps({"items": items}, ensure_ascii=False))


if __name__ == "__main__":
    main()
