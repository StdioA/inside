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

const app = new Vue({
	data: {
		show: true,
		error: {status: false, message: ""},
		post_id: 0,
		previous_id: 0,
		next_id: 0,
		post: {}, 
		csrf_token: getCookie('csrftoken')
	},
	methods: {
		add_comment: function (event) {
			const app = this;
			const post_data = {
				author: $("input[name=author]").val(),
				content: $("input[name=content]").val()
			};
			fetch("/api/comment/" + this.post_id, {
				method: 'POST',
				body: JSON.stringify(post_data),
				headers: new Headers({
					'Content-Type': 'application/json',
					'X-CSRFToken': getCookie("csrftoken")
				})
			}).then(res => res.json())
			  .then(data => {
				  if (data.success) {
					  app.post.comments.push({
						  author: post_data.author,
						  content: post_data.content
					  });
					  $("input[name=author]").val("");
					  $("input[name=content]").val("");
				  }
			  }).catch(error => console.error('Error:', error));
			this.csrf_token = getCookie("csrftoken");
		},
		jump: function(event) {
			const app = this;
			let post_id;
			app.show = false;
			if (event.target.id == "pageup") {
				post_id = app.previous_id;
			}
			else if (event.target.id == "pagedown") {
				post_id = app.next_id;
			}
			fetch("api/post/" + post_id, {
				credentials: "include"
			}).then(res => res.json()).then(data => {
				app.show = true;
				app.post_id = data.post.id;
				app.post = data.post;
				app.previous_id = data.previous_id;
				app.next_id = data.next_id;
				history.pushState({}, "", "/" + post_id);
			});
		}
	},
	init: function () {
		const post_id = window.location.pathname.split("/")[1];
		const app = this;

		fetch("api/post/" + post_id, {
			credentials: "include"
		}).then(res => res.json()).then(data => {
			if (data.success) {
				app.post_id = data.post.id;
				app.post = data.post;
				app.previous_id = data.previous_id;
				app.next_id = data.next_id;
			}
			else {
				app.error.status = true;
				app.error.message = data.reason;
			}
		})
	}
});

(() => {
	// 随机背景色
	const colors = ["blue", "green", "yellow", "purple"];
	const color = colors[Math.floor(Math.random()*colors.length)];
	$("body").addClass("bg-"+color);

	app.$mount("#content_bg");
})();

