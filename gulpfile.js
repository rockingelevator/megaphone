var gulp = require('gulp');
var stylus = require('gulp-stylus');
var concatCss = require('gulp-concat-css');
var minifyCss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var watchify = require('watchify');
var gutil = require('gulp-util');
var source = require('vinyl-source-stream');
var browserify = require('browserify');
var reactify = require('reactify');


gulp.task('stylus', function() {
    gulp.src('./styl/**/*.styl')
        .pipe(stylus())
    .pipe(gulp.dest('./static/css'));
});

gulp.task('cssBuild', function(){
    gulp.src('./static/css/**/*.css')
        .pipe(concatCss('main.css'))
        .pipe(minifyCss())
        .pipe(gulp.dest('./static/dist/css'))
});

gulp.task('js', function(){
    gulp.src('./static/scripts/**/*.js')
        .pipe(concat('build.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./static/dist/js'))
});

gulp.task('default', function(){
    var bundler = watchify(browserify({
        entries: ['./static/scripts/components/app.jsx'],
        transform: [reactify],
        extensions: ['.jsx'],
        debug: true,
        cache: {},
        packageCache: {},
        fullPaths: true
    }));

    function build(file) {
        if(file) gutil.log('Recompiling ' + file);
        return bundler
            .bundle()
            .on('error', gutil.log.bind(gutil, 'Browserify Error'))
            .pipe(source('main.js'))
            .pipe(gulp.dest('./static/scripts/'));
    };

    build();
    bundler.on('update', build);

    //gulp.start('stylus', 'cssBuild');
    gulp.watch('./styl/**/*.styl', ['stylus']);
});



