"use strict";

$(document).ready(function () {
	$("#form button").on("click", function (event) {
		var post_id = $("#content_bg").attr("post-id");
		var url = "/api/"+post_id+"/";
		var button = event.target;
		if (button.id == "update") {
			$.post(url, {
							"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
							"content": $("textarea").first().val()
						}, 
					function (data, success) {
						$("#update").addClass("green");
						setTimeout(function () {
							$("#update").removeClass("green");
						}, 1000);
					});
		}
		else if (button.id == "delete") {
			$.ajax({
				url: url,
				type: "DELETE",
				beforeSend: function (xhr) {
					xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
				},
				success: function (data) {
					console.log(data);
					$("#delete").addClass("green");
					setTimeout(function () {
						$("#delete").removeClass("green");
					}, 1000);
				}
			});
		}
	});
});
