#!/bin/bash

echo '### Workflow version'
/usr/libexec/PlistBuddy -c 'Print :version' info.plist

echo
echo '### Alfred version'
/usr/bin/osascript -e 'tell application id "com.runningwithcrayons.Alfred" to return version'

echo
echo '### macOS version'
/usr/bin/sw_vers -productVersion

echo
echo '### Architecture'
/usr/bin/arch
echo

echo
echo '### Preferences'

excluded_vars=(labels)
for i in {1..6}; do
    excluded_vars+=("fastphrase${i}")
done
for i in {0..9}; do
    excluded_vars+=("email_${i}")
done

if [[ -f 'prefs.plist' ]]; then
    /usr/bin/python3 - <<'PY'
import plistlib
import sys

excluded = {
    *{f"labels_{i}" for i in range(10)},
    *{f"fastphrase{i}" for i in range(1, 7)},
    *{f"email_{i}" for i in range(10)},
}


def redact(value):
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items() if key not in excluded}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


with open("prefs.plist", "rb") as fh:
    prefs = plistlib.load(fh)

plistlib.dump(redact(prefs), sys.stdout.buffer, fmt=plistlib.FMT_XML, sort_keys=False)
PY
else
    echo 'Default'
fi

echo
echo '### Full Disk Access'

if [[ "$(sqlite3 '/Library/Application Support/com.apple.TCC/TCC.db' 'SELECT EXISTS (SELECT 1 FROM access WHERE auth_value AND service = "kTCCServiceSystemPolicyAllFiles" AND client = "com.runningwithcrayons.Alfred")')" -eq 1 ]]; then
    echo 'Granted'
else
    echo 'NOT granted'
fi

echo
echo '### Cache dir'

readonly cache_files="$(ls -1 "${alfred_workflow_cache}")"

if [[ -n "${cache_files}" ]]; then
    echo "${cache_files}"
else
    echo 'Files NOT present'
fi

echo
echo '### Cache file'

if [[ -f "${alfred_workflow_cache}/cache.db" ]]; then
    stat "${alfred_workflow_cache}/cache.db"
else
    echo 'Does NOT exist'
fi

echo
echo '### Temporary cache'

if [[ -f "${alfred_workflow_cache}/tmp.db" ]]; then
    stat "${alfred_workflow_cache}/tmp.db"
else
    echo 'Does NOT exist'
fi

echo
echo '### Build progress'

if ps A | grep --quiet '[r]uby.*Alfred.*rebuild_cache'; then
    echo 'Running'
else
    echo 'NOT running'
fi

echo
echo '### Launchd job'

if launchctl list | grep -q "${alfred_workflow_bundleid}"; then
    echo -n 'Loaded: '
    launchctl list | grep "${alfred_workflow_bundleid}"
else
    echo 'NOT loaded'
fi

if [[ -f "${HOME}/Library/LaunchAgents/${alfred_workflow_bundleid}.plist" ]]; then
    echo 'Installed'
else
    echo 'NOT installed'
fi

echo
echo '### Workflow custom variables'

excluded_vars=(labels)
for i in {0..9}; do
    excluded_vars+=("email_${i}")
done

for var_name in gms_key gmu_key gmo_key gmss_key gmuu_key gmoo_key gmsettings_key userNumber labels email_0 email_1 email_2 email_3 email_4 email_5 email_6 email_7 email_8 email_9; do
    skip_var=false
    for excluded_var in "${excluded_vars[@]}"; do
        if [[ "${var_name}" == "${excluded_var}" ]]; then
            skip_var=true
            break
        fi
    done

    if [[ "${skip_var}" == true ]]; then
        continue
    fi

    var_value="${!var_name}"
    if [[ -n "${var_value}" ]]; then
        echo "${var_name}=${var_value}"
    else
        echo "${var_name}=<unset>"
    fi
done
