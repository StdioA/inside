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
			// setTimeout(function () {
				
			// }, 3000);
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

	console.log(lat);

	$.get("/api/archive/"+lat, function (data) {
		app.posts = data.posts;
		app.$mount("#archives");
		app.ready = true;
	});
});
