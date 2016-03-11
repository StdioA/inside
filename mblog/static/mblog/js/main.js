"use strict";

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var app = new Vue({
	data: {
		show: true,
		post_id: 0,
		post: {}, 
		csrf_token: getCookie('csrftoken')
	},
	methods: {
		add_comment: function (event) {
			var app = this;
			var post_data = {
				csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
				author: $("input[name=author]").val(),
				content: $("input[name=content]").val()
			};
			$.post("/api/"+this.post_id+"/comment", post_data, function (data) {
				if (data.success) {
					app.post.comments.push({
						author: post_data.author,
						content: post_data.content
					});
					$("input[name=author]").val("");
					$("input[name=content]").val("");
				}
			}, "JSON");
			this.csrf_token = getCookie('csrftoken');
		},
		jump: function (event) {
			var post_id;
			this.show = false;
			if (event.target.id == "pageup") {
				post_id = this.post.previous_id;
			}
			else if (event.target.id == "pagedown") {
				post_id = this.post.next_id;
			}
			$.getJSON("/api/"+post_id+"/", function (data, status) {
				app.show = true;
				app.post_id = post_id;
				app.post = data;
				history.pushState({}, "", "/"+post_id);
			});
		}
	}
});

$(document).ready(function () {
	var post_id = window.location.pathname.split("/")[1];
	$.getJSON("/api/"+post_id+"/", function (data, status) {
		app.post_id = post_id;
		app.post = data;
		app.$mount("#content_bg");
	});
});

