"use strict";

var app = new Vue({
	data: {
		ready: false,
		posts: []
	},
	methods: {
		click: function (event) {
			var post = event.target.id.replace("post-", "")
			console.log("/"+post);
			location.href = "/"+post;
		},
		get_summary: function (post) {
			console.log(1);
			var summary = post.content.split("\n").slice(0,3).map(function (line) {
					if (line.length>40) {
						line = line.slice(0,40)+"…";
					}
					return line;
				});
			return summary;
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

