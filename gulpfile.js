var gulp = require('gulp'),
    bs = require('browser-sync').create();

var staticPath = 'static';

var np = 'node_modules';

gulp.task('copy', function () {
    var mdlicons = np + '/material-design-icons-iconfont/dist';

    return [
        gulp.src([np + '/materialize-css/dist/**/*'])
            .pipe(gulp.dest(staticPath)),

        gulp.src([mdlicons + '/**/*'], { base: mdlicons })
            .pipe(gulp.dest(staticPath + '/fonts/material-iconfont')),

        gulp.src([np + '/jquery/dist/*.js'])
            .pipe(gulp.dest(staticPath + '/js'))
    ];
});

gulp.task('browser-sync', function () {
    bs.init({
        files: [
            staticPath + '/css/*.css',
            staticPath + '/js/*.js',
            '*/templates/**/*.html',
            '*/**/*.py',
            '!venv/**/*'
        ],
        proxy: '127.0.0.1:8000',
        reloadDebounce: 500,
        reloadDelay: 300
    });
});


gulp.task('default', ['copy', 'browser-sync']);
gulp.task('run', ['browser-sync']);
