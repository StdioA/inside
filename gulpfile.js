const gulp  = require('gulp');
const babel = require('gulp-babel');
const uglify = require('gulp-uglify');
const uglifycss = require('gulp-uglifycss');
const rename = require('gulp-rename');
const less = require('gulp-less')
const clean = require('gulp-clean')


const js_output = './mblog/static/mblog/js/'
const css_output = './mblog/static/mblog/css/'

gulp.task("babel", () => {
	gulp.src('./mblog/static/mblog/js/!(*.min).js')
		.pipe(babel({
			presets: ['@babel/env']
		}))
		.pipe(rename({ suffix: ".babel" }))
		.pipe(gulp.dest(js_output))
});

gulp.task("compress-js", ["babel"], () => {
	return gulp.src('./mblog/static/mblog/js/*.babel.js')
			.pipe(uglify())
			.pipe(rename((path) => {
				path.basename = path.basename.replace("babel", "min");
			}))
		.pipe(gulp.dest(js_output))
});

gulp.task("less", [], () => {
	return gulp.src('./mblog/static/mblog/less/*.less')
			.pipe(less())
			.pipe(gulp.dest(css_output))
});

gulp.task("compress-css", ["less"], () => {
	return gulp.src('./mblog/static/mblog/css/!(*.min).css')
			.pipe(uglifycss())
			.pipe(rename({ suffix: ".min" }))
			.pipe(gulp.dest(css_output))
});

gulp.task('watch', ["compress-js", "compress-css"], () => {
	var watcher_js = gulp.watch('./mblog/static/mblog/js/*.js', ['compress-js']);
	var watcher_css = gulp.watch('./mblog/static/mblog/less/*.less', ['less', 'compress-css']);
	
	watcher_js.on('change', function (event) {
		console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
	});
	
	watcher_css.on('change', function (event) {
		console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
	});
});

gulp.task('compress', ['compress-js', 'compress-css']);
gulp.task('clean', ['compress'], () => {
	return gulp.src('./mblog/static/mblog/js/*babel*.js')
			   .pipe(clean());
});

gulp.task('default', ['compress', 'clean']);
