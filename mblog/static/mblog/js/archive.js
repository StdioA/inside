"use strict";

var app = new Vue({
	data: {
		ready: false,
		posts: []
	}
});

$(document).ready(function () {
	var lat = Number(location.hash.replace("#", ""));
	if (Object.is(lat, NaN) || lat <= 0) {
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
