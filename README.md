# Gmail Search Tools

Alfred workflow for quick access to Gmail search.

## Keywords

- **`gms`** — Search Gmail messages (customisable)
- **`gmu`** — Search unread Gmail messages (customisable)

## Usage

Type `gms` followed by your search query to search across Gmail messages with multiple filter options.

Type `gmu` followed by your search query to search only unread messages.

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

Customise the keywords and Gmail account in Alfred's workflow preferences:

| Variable | Default | Description |
|---|---|---|
| `keyword` | `gms` | Main Gmail search keyword |
| `unread_keyword` | `gmu` | Unread Gmail search keyword |
| `gmail_account` | `0` | Gmail account index (0 = primary, 1 = second account) |

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

# Build the workflow
npm run build
```

The built workflow file will be at `dist/alfred-gmail-search.alfredworkflow`.

## License

MIT License — see [LICENSE](LICENSE).
