const gulp = require('gulp');
const fs = require('fs');
const path = require('path');
const gulpZip = require('gulp-zip');
const del = require('del');
const { exec } = require('child_process');

// Clean build directory
gulp.task('clean', () => del(['dist/**', 'cache/**']));

// Run Python tests
gulp.task('test', (done) => {
    exec('.venv/bin/python3 -m pytest tests/ -v', (err, stdout, stderr) => {
        console.log(stdout);
        console.error(stderr);
        done(err);
    });
});

// Copy source files to dist
gulp.task('copy-src', () => {
    return gulp.src([
        'src/**/*',
        '!src/**/__pycache__/**',
        '!src/**/*.pyc',
    ], { base: 'src' })
        .pipe(gulp.dest('dist/alfred-gmail-search'));
});

// Copy root icon to dist
gulp.task('copy-icon', () => {
    return gulp.src('icon.png')
        .pipe(gulp.dest('dist/alfred-gmail-search'));
});

// Combined copy task
gulp.task('copy', gulp.series('copy-src', 'copy-icon'));

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
    return gulp.src('dist/alfred-gmail-search/**/*')
        .pipe(gulpZip('alfred-gmail-search.alfredworkflow'))
        .pipe(gulp.dest('dist'));
});

// Build workflow
gulp.task('build', gulp.series('clean', 'create-dirs', 'test', 'copy', 'package'));

// Watch for changes
gulp.task('watch', () => {
    gulp.watch('src/**/*', gulp.series('copy'));
});

// Development task
gulp.task('dev', gulp.series('clean', 'create-dirs', 'copy', 'watch'));

// Default task
gulp.task('default', gulp.series('build'));
