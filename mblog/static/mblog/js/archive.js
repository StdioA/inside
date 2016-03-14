"use strict";

var app = new Vue({
	data: {
		ready: false,
		posts: [],
		more_lock: false,
		posts_end: false
	},
	methods: {
		click: function (event) {
			var post = event.target.id.replace("post-", "")
			location.href = "/"+post;
		},
		get_summary: function (post) {
			var summary = post.content.split("\n").slice(0,3).map(function (line) {
					if (line.length>40) {
						line = line.slice(0,40)+"…";
					}
					return line;
				});
			return summary;
		},
		get_more: function (event) {
			var count = 6;							// 每次获取的post数量
			var app = this;
			if (app.posts_end) {
				return;
			}

			var last_id = this.posts[this.posts.length-1].id-1;

			// 加锁，防止多次触发get_more导致获取重复数据
			if (!app.more_lock) {
				app.more_lock = true;

				$.get("api/archive/"+last_id+"/counts/"+count, function (data) {
					app.posts = app.posts.concat(data.posts);
					if (data.posts.length != count) {
						app.posts_end = true;
					}
					app.more_lock = false;
				});
			}
		}
	}
});

$(document).ready(function () {
	var lat = Number(location.hash.replace("#", ""));
	if (isNaN(lat) || lat <= 0) {
		lat = "";
	}
	else {
		lat = String(lat);
	}

	$.get("/api/archive/"+lat, function (data) {
		app.posts = data.posts;
		app.$mount("#archives");
		app.ready = true;
	});
});

