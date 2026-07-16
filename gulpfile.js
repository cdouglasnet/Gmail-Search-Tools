const gulp = require('gulp');
const fs = require('fs');
const gulpZip = require('gulp-zip');
const del = require('del');
const { execFile } = require('child_process');
const { resolvePythonBin } = require('./scripts/run-python');

const WORKFLOW_SOURCE = process.env.npm_config_workflow_source || process.env.WORKFLOW_SOURCE || 'src';
const DIST_NAME = process.env.npm_config_dist_name || process.env.DIST_NAME || 'gmail-search-tools';
const DIST_DIR = `dist/${DIST_NAME}`;
const WORKFLOW_FILE = process.env.npm_config_workflow_file || process.env.WORKFLOW_FILE || `${DIST_NAME}.alfredworkflow`;
const PYTHON_BIN = resolvePythonBin();

// Clean build directory
gulp.task('clean', () => del(['dist/**', 'cache/**']));

// Run Python tests
gulp.task('test', (done) => {
    execFile(PYTHON_BIN, ['-m', 'pytest', 'tests/', '-v'], (err, stdout, stderr) => {
        console.log(stdout);
        console.error(stderr);
        done(err);
    });
});

// Copy source files to dist
gulp.task('copy-src', () => {
    return gulp.src([
        `${WORKFLOW_SOURCE}/**/*`,
        `!${WORKFLOW_SOURCE}/**/__pycache__/**`,
        `!${WORKFLOW_SOURCE}/**/*.pyc`,
    ], { base: WORKFLOW_SOURCE })
        .pipe(gulp.dest(DIST_DIR));
});

// Copy root workflow assets to dist
gulp.task('copy-assets', () => {
    return gulp.src(['*.png', '*.icns', 'Icon'], { allowEmpty: true })
        .pipe(gulp.dest(DIST_DIR));
});

// Combined copy task
gulp.task('copy', gulp.series('copy-src', 'copy-assets'));

// Create needed directories
gulp.task('create-dirs', (done) => {
    const dirs = ['cache', 'dist'];

    dirs.forEach(dir => {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
    });

    done();
});

// Package workflow
gulp.task('package', () => {
    return gulp.src(`${DIST_DIR}/**/*`)
        .pipe(gulpZip(WORKFLOW_FILE))
        .pipe(gulp.dest('dist'));
});

// Build workflow
gulp.task('build', gulp.series('clean', 'create-dirs', 'test', 'copy', 'package'));

// Watch for changes
gulp.task('watch', () => {
    gulp.watch([`${WORKFLOW_SOURCE}/**/*`, '*.png', '*.icns', 'Icon'], gulp.series('copy'));
});

// Development task
gulp.task('dev', gulp.series('clean', 'create-dirs', 'copy', 'watch'));

// Default task
gulp.task('default', gulp.series('build'));
