var gulp = require('gulp');
var stylus = require('gulp-stylus');
var minifyCss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');

gulp.task('stylus', function() {
    gulp.src('./styl/**/*.styl')
        .pipe(stylus())
    .pipe(gulp.dest('./static/css'))
});

gulp.task('cssBuild', function(){
    gulp.src('./static/css/**/*.css')
        .pipe(minifyCss())
        .pipe(gulp.dest('./static/dist/css'))
});

gulp.task('js', function(){
    gulp.src('./static/scripts/**/*.js')
        .pipe(concat('build.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./static/dist/js'))
});

gulp.task('default', ['stylus', 'cssBuild', 'js']);