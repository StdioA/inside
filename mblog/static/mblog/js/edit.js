"use strict";

const getCSRFToken = () => {
  return document.querySelector("input[name=csrfmiddlewaretoken]").value
}

(() => {
  const clickListener = (event) => {
    const post_id = $("#content_bg").attr("post-id");
    const url = "/api/post/" + post_id;
    const button = event.target;
    const headers = new Headers({
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()
    })

    if (button.id == "update") {
      const payload = {
        content: $("textarea").first().val(),
        exist: document.getElementsByName("exist")[0].checked
      }
      fetch(url, {
        method: "PUT",
        body: JSON.stringify(payload),
        headers: headers,
      }).then(res => res.json())
        .then(data => {
          $("#update").addClass("green");
          setTimeout(function () {
            $("#update").removeClass("green");
          }, 1000);
        });
    } else if (button.id == "delete") {
      fetch(url, {
        method: "DELETE",
        headers: headers,
      }).then(res => res.json())
        .then(data => {
          $("#delete").addClass("green");
          setTimeout(function () {
            $("#delete").removeClass("green");
          }, 1000);
        });
    }
  };
  document.querySelector("#form button#update").addEventListener("click", clickListener);
  document.querySelector("#form button#delete").addEventListener("click", clickListener);
  document.querySelector("#comment button").addEventListener("click", (event) => {
    const post_id = $("#content_bg").attr("post-id");
    const url = "/api/comment/" + post_id;
    fetch(url, {
      method: 'POST',
      body: JSON.stringify({
        author: $("input[name=author]").val(),
        content: $("input[name=content]").val()
      }),
      headers: new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      })
    }).then(res => res.json())
      .then(data => {
        if (data.success == true) {
          $("#comment button").addClass("green");
          setTimeout(function () {
            $("#comment button").removeClass("green");
          }, 1000);
        }
      })
  });
})();
