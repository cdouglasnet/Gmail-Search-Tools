const fs = require('fs');
const { spawnSync } = require('child_process');

function resolvePythonBin() {
    if (process.env.PYTHON) {
        return process.env.PYTHON;
    }

    const venvPython = '.venv/bin/python3';
    if (fs.existsSync(venvPython)) {
        return venvPython;
    }

    return 'python3';
}

function main() {
    const result = spawnSync(resolvePythonBin(), process.argv.slice(2), {
        stdio: 'inherit',
    });

    if (result.error) {
        console.error(result.error.message);
        process.exit(1);
    }

    process.exit(result.status ?? 1);
}

if (require.main === module) {
    main();
}

module.exports = { resolvePythonBin };
