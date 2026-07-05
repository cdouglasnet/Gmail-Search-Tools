# Gmail Search Tools

[![Production Release](https://img.shields.io/github/actions/workflow/status/cdouglasnet/Gmail-Search-Tools/ci.yml?branch=main&label=Production%20Release)](https://github.com/cdouglasnet/Gmail-Search-Tools/actions/workflows/ci.yml?query=branch%3Amain)
[![Beta Release](https://img.shields.io/github/actions/workflow/status/cdouglasnet/Gmail-Search-Tools/ci.yml?branch=dev&label=Beta%20Release)](https://github.com/cdouglasnet/Gmail-Search-Tools/actions/workflows/ci.yml?query=branch%3Adev)
[![Version](https://img.shields.io/github/v/release/cdouglasnet/Gmail-Search-Tools?label=Version)](https://github.com/cdouglasnet/Gmail-Search-Tools/releases)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](requirements.txt)
[![Alfred](https://img.shields.io/badge/Alfred-5%2B-5C1F87)](https://www.alfredapp.com/)
[![License](https://img.shields.io/github/license/cdouglasnet/Gmail-Search-Tools?label=License)](LICENSE)

Alfred workflow for quick access to Gmail search.

![Alt text](icon.png)

## Keywords

- **`gms`** — Search Gmail messages (customizable)
- **`gmu`** — Search unread Gmail messages (customizable)
- **`gmo`** — Gmail Search Operators (customizable)
- **`gmsettings`** — Workflow settings/actions menu (customizable)

## Usage

Type `gms` followed by your search query to search across Gmail messages with multiple filter options.

Type `gmu` followed by your search query to search only unread messages.

Type `gmo` to browse Gmail search operators and quick actions.

Type `gmsettings` to open the workflow settings/actions menu (Config, Diagnostic, Forum, GitHub).

### `gms` search options
- **Search Gmail** — search all messages
- **Search Unread** — search unread messages only
- **Search Starred** — search starred messages
- **Search Sent** — search sent messages
- **Search Drafts** — search draft messages
- **Search Important** — search important messages
- **Search Spam** — search spam messages
- **Search Trash** — search trash messages

### `gmu` search options
- **Search Unread Gmail** — all unread messages
- **Search Unread in Inbox** — unread inbox messages
- **Search Unread Important** — unread important messages
- **Search Unread Starred** — unread starred messages

## Configuration

Customize keywords and Gmail account in Alfred's workflow preferences:

| Variable | Default | Description |
|---|---|---|
| `gms_key` | `gms` | Main Gmail search keyword |
| `gmu_key` | `gmu` | Unread Gmail search keyword |
| `gmo_key` | `gmo` | Gmail Search Operators keyword |
| `gmsettings_key` | `gmsettings` | Settings/actions menu keyword |
| `gmss_key` | - | Secondary Gmail search keyword (optional) |
| `gmuu_key` | - | Secondary unread Gmail search keyword (optional) |
| `userNumber` | `0` | Gmail account index (0 = primary, 1 = second account, etc.) |

## TODO

- Update the Forum menu URL in `src/info.plist` to the dedicated Gmail Search Tools forum thread once it is posted.

## Installation

1. Download `alfred-gmail-search.alfredworkflow` from the [releases page](https://github.com/cdouglasnet/Gmail-Search-Tools/releases)
2. Double-click to install in Alfred
3. Use `gms` to start searching Gmail

## Building from Source

Requires Node.js and Python 3.9+.

```bash
# Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install

# Run tests
npm test

# Build the workflow (uses `tmp/` by default)
npm run build

# Build from `src/` instead
npm run build:src
```

The built workflow file will be at `dist/alfred-gmail-search.alfredworkflow`.

## License

MIT License — see [LICENSE](LICENSE).
