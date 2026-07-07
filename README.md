# Gmail Search Tools

[![Production Release](https://img.shields.io/github/actions/workflow/status/cdouglasnet/Gmail-Search-Tools/ci.yml?branch=main&label=Production%20Release)](https://github.com/cdouglasnet/Gmail-Search-Tools/actions/workflows/ci.yml?query=branch%3Amain)
[![Beta Release](https://img.shields.io/github/actions/workflow/status/cdouglasnet/Gmail-Search-Tools/ci.yml?branch=dev&label=Beta%20Release)](https://github.com/cdouglasnet/Gmail-Search-Tools/actions/workflows/ci.yml?query=branch%3Adev)
[![Version](https://img.shields.io/github/v/release/cdouglasnet/Gmail-Search-Tools?label=Version)](https://github.com/cdouglasnet/Gmail-Search-Tools/releases)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](requirements.txt)
[![Alfred](https://img.shields.io/badge/Alfred-5%2B-5C1F87)](https://www.alfredapp.com/)
[![License](https://img.shields.io/github/license/cdouglasnet/Gmail-Search-Tools?label=License)](LICENSE)

[![counter](https://img.shields.io/github/downloads/cdouglasnet/Gmail-Search-Tools/latest/total)](https://github.com/cdouglasnet/Gmail-Search-Tools/releases)
[![counter](https://img.shields.io/github/downloads/cdouglasnet/Gmail-Search-Tools/total)](https://github.com/cdouglasnet/Gmail-Search-Tools/releases)

Alfred Workflow for quick access to Gmail Searching, Starred, Un-Read, and more.

![Alt text](icon.png)

## 🔍 Keywords - (Customizable in Configuration)

- **`gms`** — Gmail Search Messages, Stars (Filterable) 🔍
- **`gmss`** — Gmail Search Messages with argument ⭐️
- **`gmu`** — Gmail Un-Read Messages (Filterable) 📬
- **`gmuu`** — Search unread Gmail messages with argument 📩
- **`gmo`** — Gmail Search Operators (Filterable) 🧰
- **`gmoo`** — Gmail Search Operators with argument ⚙️
- **`gmsettings`** — Workflow settings/actions menu 🛠️

## 🚦 Usage

- `gms`<kbd>↩</kbd> Filterable List ➡️ default search. i.e. URL + has:red-bang
- `gmss` `{query}`<kbd>↩</kbd> Search + query ➡️ i.e. URL + has:red-bang + mySearchTerm(s)
- `gmu`<kbd>↩</kbd> Filterable List ➡️ default search Un-Read Messages. i.e. URL + is:unread
- `gmuu` `{query}`<kbd>↩</kbd> Un-Read + query ➡️ i.e. URL + is:unread + mySearchTerm(s)
- `gmo`<kbd>↩</kbd> Filterable List Search Operators ➡️ i.e. URL + has:attachment
- `gmoo` `{query}`<kbd>↩</kbd> Search Operators + query ➡️ i.e. URL + has:attachment + mySearchTerm(s)
- `gmsettings`<kbd>↩</kbd> Open settings menu ➡️ (Config, Diagnostic, Forum, GitHub).

### `gms` search options
- **Search Gmail** — 🔍 Default search all messages
- **Unread** — 📬 Jumps to `gmu` search
- **Starred** — ⭐ yellow-star, red-star, blue-star, green-star, orange-star, purple-star,
  ❗️red-bang, yellow-bang, purple-question, blue-info, orange-guillemet, ✅ green-checkmark
- **Sent** — 📨 search sent messages
- **Drafts** — 📄 search draft messages
- **Important** — 🛟 search important messages
- **Spam** — 🍗 search spam messages
- **Trash** — 🗑️ search trash messages

### `gmu` Search Un-Read Messages Faster
- **Un-Read All** — all Un-Read messages in the main inbox
- **Un-Read Primary** — Un-Read inbox messages
- **Un-Read Updates** — Un-Read updates messages
- **Un-Read Promotions** - Un-Read promotions messages
- **Un-Read Forums** — Un-Read forums messages
- **Un-Read Reservations** - Un-Read reservations messages
- **Un-Read Purchases** — Un-Read purchases messages
- **Search Unread Starred** — unread starred messages

### `gmo` Search Operators
- **To/From** - 🕵️‍♀️ To: or From:
- **Subject** - 👀 Subject: (search within subject line)
- **Label** - 🏷️ label: (search within a specific label) i.e. label:myLabel
- **Attachment** - 💾 has:attachment (any file attachment)
- **Drive Links** - ☁️ has:drive (Google Drive links)
- **Video** - ▶️ has:YouTube (YouTube video links)
- **Document** - 📄 has:document (Google Docs, Word, PDF)
- **Spreadsheet** - 📊 has:spreadsheet (Excel, Numbers, Sheets)
- **Presentation** - 🖥️ has:presentation (PowerPoint, Keynote, Slides)

## ⚙️ Configuration

Customize keywords and Gmail account in Alfred's workflow preferences:

| Variable         | Default      | Description                                                 |
|------------------|--------------|-------------------------------------------------------------|
| `gms_key`        | `gms`        | Main Gmail search keyword                                   |
| `gmu_key`        | `gmu`        | Unread Gmail search keyword                                 |
| `gmo_key`        | `gmo`        | Gmail Search Operators keyword                              |
| `gmss_key`       | `gmss`       | Search Keyword (With Argument)                              |
| `gmuu_key`       | `gmuu`       | Un-Read keyword (With Argument)                             |
| `gmoo_key`       | `gmoo`       | Gmail Operators (With Argument)                             |
| `gmsettings_key` | `gmsettings` | Settings/actions menu keyword                               |
| `userNumber`     | `0`          | Gmail account index (0 = primary, 1 = second account, etc.) |

## 🔒 Security
- No special permissions are needed - uses links sent to the browser. (Defaults to Chrome)
- The workflow does not need Gmail credentials at all! 100% safe.
- Just make sure your browser is signed in to your Gmail account.

## 📋 TODO

- Update the Alfred Forum URL in `src/info.plist` to the dedicated Gmail Search Tools forum thread once it is posted.

## ⚙️ Installation

1. Download `alfred-gmail-search.alfredworkflow` from the [release page](https://github.com/cdouglasnet/Gmail-Search-Tools/releases)
2. Double-click to install in Alfred
3. Use `gms`, `gmu`, `gmo` to start searching Gmail or configure keywords in workflow preferences.

-----
## 🏗️ Building from Source

Requires Node.js and Python 3.9+.

```bash
# Install dependencies
npm run install-python-deps
npm install

# Run tests
npm test

# Build the workflow from `src/`
npm run build
```

The built workflow file will be at `dist/alfred-gmail-search.alfredworkflow`.

### IDE setup

If your editor reports standard-library imports such as `argparse`, `json`, `os`,
or `urllib` as missing, select the project virtual environment as the Python
interpreter:

```text
.venv/bin/python3
```

The included `pyrightconfig.json` points Python language servers at that virtual
environment and adds `src/script` to the import path for tests and workflow
scripts.

## ⚖️ License

MIT License — see [LICENSE](LICENSE).

Enjoy!
#### [CDoug](https://github.com/cdouglasnet)
