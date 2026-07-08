#!/usr/bin/env python3

import argparse
import json
import os

from urllib.parse import quote_plus

GMAIL_BASE_URL = "https://mail.google.com/mail/u/{account}/#search/{query}"
GMAIL_BASE_URL2 = "https://mail.google.com/mail/u/{account}/#search/{turl}+{query}"
STATIC_ICONS = {
    "gms-unread-menu": "unread.png",
    "gms-any-star": "any-star.png",
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
    "gms-back": "back.png",
    "gmu-main": "unread.png",
    "gmu-promotions": "green-money.png",
    "gmu-purchases": "green-money.png",
    "gmu-social": "social.png",
    "gmu-forums": "forums.png",
    "gmu-search-unread": "unread.png",
    "gmu-settings": "settings.png",
    "gmu-back": "back.png",
    "gmo-from": "mailfrom.png",
    "gmo-to": "mailto.png",
    "gmo-cc": "mailcc.png",
    "gmo-bcc": "mailbcc.png",
    "gmo-label": "labels.png",
    "gmo-attachments": "attachment.png",
    "gmo-drive-link": "gdrive.png",
    "gmo-document": "document.png",
    "gmo-spreadsheet": "spreadsheet.png",
    "gmo-presentation": "presentation.png",
    "gmo-youtube": "video.png",
    "gmo-filename": "filename.png",
    "gmo-user-label": "labels-any.png",
    "gmo-no-user-labels": "labels-none.png",
    "gmo-after": "date.png",
    "gmo-before": "date.png",
    "gmo-older": "date.png",
    "gmo-newer": "date.png",
    "gmo-older-than": "date.png",
    "gmo-chat": "chat.png",
    "gmo-reservations-category": "reservations.png",
    "gmo-unread": "unread.png",
    "gmo-back": "back.png",
    "gmo-settings": "settings.png",
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
    """Get the current currency icon based on Alfred environment variable"""
    currency = os.environ.get("currency", "dollar")
    return CURRENCY_ICONS.get(currency, CURRENCY_ICONS["dollar"])


def get_icon_for_uid(uid):
    """Get icon file for an uid, including currency-based icons"""
    if uid in STATIC_ICONS:
        return STATIC_ICONS[uid]
    if uid in ("gmu-promotions", "gmu-purchases", "gmo-promotions-category", "gmo-purchases-category"):
        return get_currency_icon()
    return None

# Gmail can have multiple accounts logged in at a time. The account number is used to differentiate the accounts.
def account_number():
    return os.environ.get("userNumber") or os.environ.get("gmail_account") or "0"

def turl_info():
    return os.environ.get("turl") or ""

def ticon_info():
    return os.environ.get("ticon") or ""


def gmail_url(query):
    return GMAIL_BASE_URL.format(account=account_number(), query=quote_plus(query))

def gmail_url2(query, turl):
    return GMAIL_BASE_URL2.format(account=account_number(), query=quote_plus(query), turl=quote_plus(turl))

def gmail_arg(query):
    return query

# Set Alfred Variable turl to quote_plus(query)
def set_turl(query):
    return f"setvar turl \"{quote_plus(query)}\""

def item(uid, title, subtitle, arg=None, route: str = "", url: str = "", valid=True, order=True,  icon: str = ""):
    if order:
        result = {
            "title": title,
            "subtitle": subtitle,
            "valid": valid,
            "arg": arg,
            "skipknowledge": True,  #Useful for keeping the order of the items uid cannot be used at the same time
            "maintainOrder": order,
            "icon": {"path": icon},
            "variables": {"account": account_number(), "route": route if route else "", "url": url if url else "", "ticon": icon},
        }
    else:
        result = {
            "title": title,
            "subtitle": subtitle,
            "valid": valid,
            "uid": uid, # Items will be sorted by usage in Alfred
            "arg": arg,
            "maintainOrder": order,
            "icon": {"path": icon},
            "variables": {"account": account_number(), "route": route if route else "", "url": url if url else "", "ticon": icon},
        }
    if arg is not None:
        result["arg"] = arg
    icon_file = get_icon_for_uid(uid)
    if icon_file:
        result["icon"] = {"path": icon_file}
        result["variables"]["ticon"] = icon_file
    return result

# Gmail Search Filterable List - Keep in this order
def gms_items():
    items = [
        item("gmo-search-options","Search Stars","⌘|⌥|⌃|⌘⇧|⌥⇧|⌃⇧ FastPhrases -- ⌘⌥ Clipboard","",valid=False),
        item("gms-any-star", "Test-Any", "Show mail with Any Star", gmail_arg("is:starred")),
        item("gms-any-star", "Any Star", "Show mail with Any Star", gmail_arg("is:starred")),
        item("gms-red-bang", "Red Bang", "Show mail with red-bang star", gmail_arg("has:red-bang")),
        item("gms-yellow-bang","Yellow Bang","Show mail with yellow-bang star",gmail_arg("has:yellow-bang")),
        item("gms-purple-question","Purple Question","Show mail with purple-question star",gmail_arg("has:purple-question")),
        item("gms-blue-info","Blue Info","Show mail with blue-info star",gmail_arg("has:blue-info")),
        item("gms-blue-star", "Blue Star", "Show mail with blue-star", gmail_arg("has:blue-star")),
        item("gms-orange-guillemet","Orange Guillemet","Show mail with orange-guillemet",gmail_arg("has:orange-guillemet")),
        item("gms-yellow-star", "Yellow Star", "Show mail with yellow-star", gmail_arg("has:yellow-star")),
        item("gms-orange-star", "Orange Star", "Show mail with orange-star", gmail_arg("has:orange-star")),
        item("gms-red-star", "Red Star", "Show mail with red-star", gmail_arg("has:red-star")),
        item("gms-purple-star", "Purple Star", "Show mail with purple-star", gmail_arg("has:purple-star")),
        item("gms-green-star", "Green Star", "Show mail with green-star", gmail_arg("has:green-star")),
        item("gms-green-check","Green Checkmark","Show mail with green-check",gmail_arg("has:green-check"), icon="checkmark.png"),
        # Menu Items To Other Searching Tools/Keywords
        item("gms-search-arg", "→ Gmail Search With Argument", "Fast Custom Search", "", route="main2"),
        item("gms-search-unread","→ Search Unread","Search Un-Read Gmail Messages","", route="unread"),
        item("gms-search-reference", "→ Gmail Search Operators", "Learn Power Searches", "", route="operators"),
        item("gms-unread-menu", "→ Un-Read Mail", "Unread quick links", "", route="unread"),
        item("gms-settings", "→ Settings", "Open workflow configuration", "", route="settings"),
    ]
    return items

# Un-Read Mail Filterable List - Keep in this order
def gmu_items():
    items = [
        item("gmu-search-unread","Search Unread","Search Un-Read Messages",gmail_arg("is:unread")),
        item("gmu-primary","Primary Unread","Unread in Primary",gmail_url("category:primary label:unread"), order=False),
        item("gmu-updates","Updates UnRead","Unread in Updates",gmail_url("category:updates label:unread"), order=False),
        item("gmu-promotions","Promotions UnRead","Unread in Promotions",gmail_url("category:promotions label:unread"), order=False),
        item("gmu-forums","Forums UnRead","Unread in Forums",gmail_url("category:forums label:unread"), order=False),
        item("gmu-reservations","Reservations","Reservations category",gmail_url("category:reservations"), order=False),
        item("gmu-purchases", "Purchases", "Purchases category", gmail_url("category:purchases"), order=False),
        # Menu Items To Other Searching Tools/Keywords
        item("gmu-search-arg", "→ Un-Read Search With Argument", "Fast Custom Un-Read Search", "", route="unread2"),
        item("gmu-settings", "→ Settings", "Open workflow configuration", "", route="settings"),
        item("gmu-back", "→ Start Over", "Return to the main menu", "", route="main"),
    ]
    return items

# Search Operators Filterable List - Keep in this order
def gmo_items():
    items = [
        item("gmo-search-options","Search Operators","⌘|⌥|⌃|⌘⇧|⌥⇧|⌃⇧ FastPhrases -- ⌘⌥ Clipboard","",valid=False),
        item("gmo-search-arg", "Gmail Operators With Argument", "Fast Operator Search", "operators2"),
        item("gmo-from", "From", "Ex. from:bob", gmail_url("from:")),
        item("gmo-to", "To", "Ex. to:bob", gmail_url("to:")),
        item("gmo-cc", "CC", "Ex. cc:bob", gmail_url("cc:")),
        item("gmo-bcc", "BCC", "Ex. bcc:bob", gmail_url("bcc:")),
        item("gmo-subject", "Subject", "Ex. subject:what about bob", gmail_url("subject:")),
        item("gmo-or", "OR", "Ex. from:bob OR from:bam", "OR"),
        item("gmo-exclude", "Exclude", "Ex. bam -rock", gmail_url("-")),
        item("gmo-around", "AROUND", "Ex. flight AROUND 10 airport", "AROUND"),
        item("gmo-label", "Label", "Ex. label:builders", gmail_url("label:")),
        item("gmo-attachments", "Attachments", "Ex. has:attachment", gmail_url("has:attachment")),
        item("gmo-drive-link", "Drive Link", "Ex. has:drive", gmail_url("has:drive")),
        item("gmo-document", "Document", "Ex. has:document", gmail_url("has:document")),
        item("gmo-spreadsheet", "Spreadsheet", "Ex. has:spreadsheet", gmail_url("has:spreadsheet")),
        item("gmo-presentation", "Presentation", "Ex. has:presentation", gmail_url("has:presentation")),
        item("gmo-youtube", "YouTube", "Ex. has:youtube", gmail_url("has:youtube")),
        item("gmo-list", "List", "Ex. list:info@example.org", gmail_url("list:")),
        item("gmo-filename", "Filename", "Ex. filename:wishlist.txt", gmail_url("filename:")),
        item("gmo-exact-word-or-phrase","Exact Word or Phrase",'Ex. "bob the builder"',gmail_url("\"\"")),
        item("gmo-group-search-terms", "Group Search Terms", "Ex. (bob builder)", gmail_url("()")), # Needs Submenu
        item("gmo-anywhere","Anywhere (include Spam & Trash)","Ex. in:anywhere",gmail_url("in:anywhere")),
        item("gmo-important", "Important", "Ex. is:important", gmail_url("is:important")),
        item("gmo-after", "After", "Ex. after:08/28/2024", gmail_url("after:")),
        item("gmo-before", "Before", "Ex. before:08/28/2004", gmail_url("before:")),
        item("gmo-older", "Older", "Ex. older:08/28/2004", gmail_url("older:")),
        item("gmo-newer", "Newer", "Ex. newer:08/28/2004", gmail_url("newer:")),
        item("gmo-older-than","Older Than (d=Day m=Mnth y=Yr)","Ex. older_than:2d",gmail_url("older_than:")),
        item("gmo-chat", "Chat", "Ex. is:chat", gmail_url("is:chat")),
        item("gmo-delivered-to","Delivered To","Ex. deliveredto:username@gmail.com",gmail_url("deliveredto:@gmail.com")),
        item("gmo-primary-category", "Primary Category", "Ex. category:primary", gmail_url("category:primary")),
        item("gmo-social-category", "Social Category", "Ex. category:social", gmail_url("category:social")),
        item("gmo-promotions-category","Promotions Category","Ex. category:promotions",gmail_url("category:promotions")),
        item("gmo-updates-category", "Updates Category", "Ex. category:updates", gmail_url("category:updates")),
        item("gmo-forums-category", "Forums Category", "category:forums", gmail_url("category:forums")),
        item("gmo-reservations-category","Reservations Category","Ex. category:reservations",gmail_url("category:reservations")),
        item("gmo-purchases-category","Purchases Category","Ex. category:purchases",gmail_url("category:purchases")),
        item("gmo-size-larger", "Size (Larger)", "Ex. size:1000000 (bytes / K / M)", gmail_url("size:")),
        item("gmo-larger-size", "Larger Size", "Ex. larger:10M", gmail_url("larger:")),
        item("gmo-smaller-size", "Smaller Size", "Ex. smaller:1M", gmail_url("smaller:")),
        item("gmo-exact-word-match", "Exact Word Match", "Ex. +unicorn", gmail_url("+")),
        item("gmo-user-label","User Label (Has Any User Label)","Ex. has:userlabels",gmail_url("has:userlabels")),
        item("gmo-no-user-labels", "No User Labels", "Ex. has:nouserlabels", gmail_url("has:nouserlabels")),
        # Menu Items To Other Searching Tools/Keywords
        item("gmo-unread", "→ Un-Read", "Un-Read quick link menu", "", route="unread"),
        item("gmo-settings", "→ Settings", "Open workflow configuration", "", route="settings"),
        item("gmo-back", "→ Start Over", "Return to the main menu", "", route="main"),
    ]
    return items

# Gmail Star Search with Qurey
def gmss_items(query):
    q = query.strip()
    items = [
        item("gmo-search-options","Gmail Search Tools","⌘|⌥|⌃|⌘⇧|⌥⇧|⌃⇧ FastPhrases -- ⌘⌥ Clipboard",valid=False),
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
        item("gms-green-check","Green Checkmark","Show mail with green-check",gmail_url("has:green-check")),
        # Menu Items To Other Searching Tools/Keywords
        item("gms-search-reference", "→ Gmail Search Reference", "Learn Power Searches", "", route="search"),
        item("gms-unread-menu", "→ Un-Read Mail", "Un-Read Quick Links Menu", "", route="unread"),
        item("gms-settings", "→ Settings", "Open workflow configuration", "", route="settings"),
        item("gms-back", "→ Start Over", "Return to the main menu", "", route="main"),
    ]
    return items



# Un-Read Mail Search With Query
def gmuu_items(query):
    q = query.strip()
    items = [
        item("gmo-search-options","Search Un-Read","⌘|⌥|⌃|⌘⇧|⌥⇧|⌃⇧ FastPhrases -- ⌘⌥ Clipboard",valid=False),
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
        # Menu Items To Other Searching Tools/Keywords
        item("gmu-settings", "→ Settings", "Open workflow configuration", "", route="settings"),
        item("gmu-back", "→ Start Over", "Return to the main menu", "", route="main"),
    ]
    return items


# Search Operators with Argument
def gmoo_items(query):
    q = query.strip()
    items = [
        item("gmo-search-options","Search Operators","⌘|⌥|⌃|⌘⇧|⌥⇧|⌃⇧ FastPhrases -- ⌘⌥ Clipboard",valid=False),
        item("gmo-from", f'From: "{q}"' if q else "From:", "Ex. from:bob", gmail_url(f"from: {q}".strip())),
        item("gmo-to", f'To: "{q}"' if q else "To:", "Ex. to:bob", gmail_url(f"to: {q}".strip())),
        item("gmo-cc", f'CC: "{q}"' if q else "CC", "Ex. cc:bob", gmail_url(f"cc: {q}".strip())),
        item("gmo-bcc", f'BCC: "{q}"' if q else "BCC", "Ex. bcc:bob", gmail_url(f"bcc: {q}".strip())),
        item("gmo-subject", f'Subject: "{q}"' if q else "Subject", "Ex. subject:what about bob", gmail_url(f"subject: {q}".strip())),
        item("gmo-or", f'OR: "{q}"' if q else "OR", "Ex. from:bob OR from:bam", gmail_url(f"OR {q}".strip()) if q else "OR"),
        item("gmo-exclude", f'Exclude: "{q}"' if q else "Exclude", "Ex. bam -rock", gmail_url(f"-{q}".strip()) if q else "-"),
        item("gmo-around", f'AROUND: "{q}"' if q else "AROUND", "Ex. flight AROUND 10 airport", gmail_url(f"{q} AROUND 10".strip()) if q else "AROUND"),
        item("gmo-label", f'Label: "{q}"' if q else "Label", "Ex. label:builders", gmail_url(f"label: {q}".strip())),
        item("gmo-attachments", f'Attachments: "{q}"' if q else "Attachments", "Ex. has:attachment", gmail_url(f"has:attachment {q}".strip())),
        item("gmo-drive-link", f'Drive Link: "{q}"' if q else "Drive Link", "Ex. has:drive", gmail_url(f"has:drive {q}".strip())),
        item("gmo-document", f'Document: "{q}"' if q else "Document", "Ex. has:document", gmail_url(f"has:document {q}".strip())),
        item("gmo-spreadsheet", f'Spreadsheet: "{q}"' if q else "Spreadsheet", "Ex. has:spreadsheet", gmail_url(f"has:spreadsheet {q}".strip())),
        item("gmo-presentation", f'Presentation: "{q}"' if q else "Presentation", "Ex. has:presentation", gmail_url(f"has:presentation {q}".strip())),
        item("gmo-youtube", f'YouTube: "{q}"' if q else "YouTube", "Ex. has:youtube", gmail_url(f"has:youtube {q}".strip())),
        item("gmo-list", f'List: "{q}"' if q else "List", "Ex. list:info@example.org", gmail_url(f"list: {q}".strip())),
        item("gmo-filename", f'Filename: "{q}"' if q else "Filename", "Ex. filename:wishlist.txt", gmail_url(f"filename: {q}".strip())),
        item(
            "gmo-exact-word-or-phrase",
            f'Exact Word or Phrase: "{q}"' if q else "Exact Word or Phrase",
            'Ex. "bob the builder"',
            gmail_url(f'"{q}"') if q else '""',
        ),
        item("gmo-group-search-terms", f'Group Search Terms: "{q}"' if q else "Group Search Terms", "Ex. (bob builder)", gmail_url(f"({q})") if q else "()"),
        item(
            "gmo-anywhere",
            f'Anywhere (include Spam & Trash): "{q}"' if q else "Anywhere (include Spam & Trash)",
            "Ex. in:anywhere",
            gmail_url(f"in:anywhere {q}".strip()) if q else "in:anywhere",
        ),
        item("gmo-important", f'Important: "{q}"' if q else "Important", "Ex. is:important", gmail_url(f"is:important {q}".strip())),
        item("gmo-after", f'After: "{q}"' if q else "After", "Ex. after:08/28/2024", gmail_url(f"after: {q}".strip())),
        item("gmo-before", f'Before: "{q}"' if q else "Before", "Ex. before:08/28/2004", gmail_url(f"before: {q}".strip())),
        item("gmo-older", f'Older: "{q}"' if q else "Older", "Ex. older:08/28/2004", gmail_url(f"older: {q}".strip())),
        item("gmo-newer", f'Newer: "{q}"' if q else "Newer", "Ex. newer:08/28/2004", gmail_url(f"newer: {q}".strip())),
        item(
            "gmo-older-than",
            f'Older Than (d=Day m=Mnth y=Yr): "{q}"' if q else "Older Than (d=Day m=Mnth y=Yr)",
            "Ex. older_than:2d",
            gmail_url(f"older_than: {q}".strip()),
        ),
        item("gmo-chat", f'Chat: "{q}"' if q else "Chat", "Ex. is:chat", gmail_url(f"is:chat {q}".strip())),
        item(
            "gmo-delivered-to",
            f'Delivered To: "{q}"' if q else "Delivered To",
            "Ex. deliveredto:username@gmail.com",
            gmail_url(f"deliveredto:@gmail.com {q}".strip()),
        ),
        item("gmo-primary-category", f'Primary Category: "{q}"' if q else "Primary Category", "Ex. category:primary", gmail_url(f"category:primary {q}".strip())),
        item("gmo-social-category", f'Social Category: "{q}"' if q else "Social Category", "Ex. category:social", gmail_url(f"category:social {q}".strip())),
        item(
            "gmo-promotions-category",
            f'Promotions Category: "{q}"' if q else "Promotions Category",
            "Ex. category:promotions",
            gmail_url(f"category:promotions {q}".strip()),
        ),
        item("gmo-updates-category", f'Updates Category: "{q}"' if q else "Updates Category", "Ex. category:updates", gmail_url(f"category:updates {q}".strip())),
        item("gmo-forums-category", f'Forums Category: "{q}"' if q else "Forums Category", "Ex. category:forums", gmail_url(f"category:forums {q}".strip())),
        item(
            "gmo-reservations-category",
            f'Reservations Category: "{q}"' if q else "Reservations Category",
            "Ex. category:reservations",
            gmail_url(f"category:reservations {q}".strip()),
        ),
        item(
            "gmo-purchases-category",
            f'Purchases Category: "{q}"' if q else "Purchases Category",
            "Ex. category:purchases",
            gmail_url(f"category:purchases {q}".strip()),
        ),
        item("gmo-size-larger", f'Size (Larger): "{q}"' if q else "Size (Larger)", "Ex. size:1000000 (bytes / K / M)", gmail_url(f"size: {q}".strip())),
        item("gmo-larger-size", f'Larger Size: "{q}"' if q else "Larger Size", "Ex. larger:10M", gmail_url(f"larger: {q}".strip())),
        item("gmo-smaller-size", f'Smaller Size: "{q}"' if q else "Smaller Size", "Ex. smaller:1M", gmail_url(f"smaller: {q}".strip())),
        item("gmo-exact-word-match", f'Exact Word Match: "{q}"' if q else "Exact Word Match", "Ex. +unicorn", gmail_url(f"+{q}".strip()) if q else "+"),
        item(
            "gmo-user-label",
            f'User Label (Has Any User Label): "{q}"' if q else "User Label (Has Any User Label)",
            "Ex. has:userlabels",
            gmail_url(f"has:userlabels {q}".strip()),
        ),
        item("gmo-no-user-labels", f'No User Labels: "{q}"' if q else "No User Labels", "Ex. has:nouserlabels", gmail_url(f"has:nouserlabels {q}".strip())),
        item("gmo-unread", f'Un-Read: "{q}"' if q else "Un-Read", "Un-Read quick link menu", gmail_url(f"is:unread {q}".strip())),
        # Menu Items To Other Searching Tools/Keywords
        item("gmo-settings", "→ Settings", "Open workflow configuration", "", route="settings"),
        item("gmo-back", "→ Start Over", "Return to the main menu", "", route="main"),
    ]
    return items


def gmsettings_items():
    return [
        item("gmsettings-config","Config →","Open workflow configuration in Alfred","", route="config"),
        item("gmsettings-diagnostic","Diagnostic →","Run workflow diagnostic","", route="diagnostic"),
        item("gmsettings-forum","Forum →","Open Alfred Forum page","", route="forum"),
        item("gmsettings-github","GitHub →","Open GitHub project page","", route="github"),
        item("gmsettings-back", "Start Over →", "Return to the main menu", "", route="back"),
    ]

# Individual Search Query Prompt and Simple Menu
def gmz_items(query):
    q = query.strip()
    z = turl_info()
    i = ticon_info()
    return [
        item("gmz-search",f'Search: "{q}"' if q else "Search:",f'Route: "{z}"' if z else "Empty Route",gmail_url2(q,z),
             route=f'Route: "{z}"' if z else "Empty Route", url=gmail_url2(q,z), icon=i),
        # Menu Items To Other Searching Tools/Keywords
        item("gmz-unread","→ Un-Read Mail","Un-Read Quick Links Menu","", route="unread"),
        item("gmz-operators","→ Search Operators","Search Operators Menu","", route="operators"),
        item("gmz-settings","→ Settings","Open workflow configuration","", route="settings"),
        item("gmsettings-back", "→ Start Over", "Return to the main menu", "", route="main"),
    ]


def main():
    parser = argparse.ArgumentParser(description="Gmail menu script filter")
    parser.add_argument(
        "--mode",
        choices=["gms", "gmss", "gmu", "gmuu", "gmo", "gmoo", "gmsettings", "gmz"],
        required=True,
    )
    parser.add_argument("--route", default="")
    parser.add_argument("query", nargs="*")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if args.mode == "gmu":
        items = gmu_items()
    elif args.mode == "gmuu":
        items = gmuu_items(query)
    elif args.mode == "gmss":
        items = gmss_items(query)
    elif args.mode == "gmo":
        items = gmo_items()
    elif args.mode == "gmoo":
        items = gmoo_items(query)
    elif args.mode == "gmsettings":
        items = gmsettings_items()
    elif args.mode == "gmz":
        items = gmz_items(query)
    else:
        items = gms_items()
    print(json.dumps({"items": items}, ensure_ascii=False))


if __name__ == "__main__":
    main()
