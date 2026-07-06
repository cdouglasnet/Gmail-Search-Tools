# 🤖 Claude Guide: Gmail Search Tools

## 📋 Project overview

Gmail Search Tools is an Alfred workflow project that provides fast Gmail search actions via script filters and browser automation.

- **🔑 Main Keywords:** `gms`, `gmu`, `gmo` (Filterable Searches)
- **🔑 Other Keywords:** `gmss`, `gmuu`, `gmoo` (Search, Un-Read, Operators w/ Argument)
- **⚙️ Settings and Debugging** `gmsettings` (Settings/Actions menu)
- **🐍 Primary runtime:** Python scripts in `src/script/`
- **📦 Packaging/build system:** Node.js + Gulp
- **⚙️ Workflow definition:** `src/info.plist`

Core Python scripts:

- `src/script/menu_filter.py` builds Alfred menu items for `gms`/`gmu`/`gmo`
- `src/script/main.py` builds Gmail search URLs and JSON items
- `src/script/utils.py` handles logging and small utility helpers

## 📚 Dependencies

### 🛠️ Runtime and tooling

- **🐍 Python:** 3.9+ (project currently uses `.venv/bin/python3` in npm scripts)
- **🟢 Node.js:** required for Gulp-based packaging
- **📦 Python packages:** `pytest` (from `requirements.txt`)
- **📦 Node dev dependencies:** `gulp`, `gulp-zip`, `del`, `eslint`, `xml2js`

### 💾 Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install
```

## 🏗️ Build, test, and dev commands

```bash
# tests
npm test

# lint Python scripts
npm run lint

# build distributable workflow in dist/
npm run build

# dev mode (copy + watch)
npm run dev
```

Build output:

- `dist/alfred-gmail-search.alfredworkflow`

## 🔒 Security considerations

- 🚫 Do not introduce secrets or account-specific data into source, tests, plist defaults, or logs.
- 🌐 Keep Gmail URL generation constrained to `https://mail.google.com/...` patterns.
- ⚠️ Treat Alfred/environment inputs (`query`, workflow variables) as untrusted input.
- 🔗 Preserve URL-encoding (`quote_plus`) when constructing Gmail search queries.
- 🐚 Avoid shelling out from Python unless strictly required; current scripts are pure Python JSON emitters.
- 📝 Logging writes to `cache/workflow.log`; avoid logging sensitive query content in production contexts.

## 🐛 Debugging workflow behavior

### ⚡ Fast checks

```bash
# Run tests
npm test

# Run script filter directly
/usr/bin/python3 src/script/menu_filter.py --mode gms "invoice"
/usr/bin/python3 src/script/menu_filter.py --mode gmu "follow up"
/usr/bin/python3 src/script/menu_filter.py --mode gmo
```

### 🎯 Common debugging targets

- ✅ Confirm JSON output shape: `{"items":[...]}` with valid Alfred item keys.
- 🖼️ Verify icon file names referenced in `menu_filter.py` exist at project root.
- 📋 Check logging output in `cache/workflow.log` when troubleshooting script behavior.
- 🔍 Validate script paths and keywords inside `src/info.plist`.

## 🎩 Alfred-specific implementation notes

- Script filters in `info.plist` execute:
  - `/usr/bin/python3 script/menu_filter.py --mode gms "{query}"`
  - `/usr/bin/python3 script/menu_filter.py --mode gmu "{query}"`
  - `/usr/bin/python3 script/menu_filter.py --mode gmo "{query}"`
- 👤 Account selection in plist is currently based on workflow variable **`userNumber`**.
- 🐍 Python `main.py` currently reads **`gmail_account`** (default `0`), while `menu_filter.py` reads `userNumber` first, then `gmail_account`.
- 🌐 Browser automation tasks match tabs by URL pattern: `https://mail.google.com/mail/u/{var:userNumber}`.

### ⚠️ Important consistency pitfall

There are two account variable names in use (`userNumber` and `gmail_account`). Prefer a single canonical variable across Python and `info.plist` when making account-routing changes to avoid mismatched Gmail account targeting.

## ✨ Best practices for future changes

- 🎯 Keep workflow behavior deterministic and side-effect light (return items, don’t mutate external state).
- 🧪 Update tests in `tests/` whenever changing search item labels, ordering, or URL generation.
- 📝 If changing keywords or script arguments, update both `src/info.plist` and docs.
- 🔄 Preserve backward compatibility for Alfred variable names unless a migration path is added.
- 🏗️ Keep build reproducible: source of truth is `src/`, package via Gulp, publish from `dist/`.
