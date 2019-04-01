"use strict";

const getCSRFToken = () => {
  return document.querySelector("input[name=csrfmiddlewaretoken]").value
}

const buttonSuccess = (dom) => {
  dom.classList.add("green");
  setTimeout(function () {
    dom.classList.remove("green");
  }, 1000);
}


(() => {
  const post_id = document.querySelector("#content_bg").getAttribute("post-id");
  const clickListener = (event) => {
    const url = "/api/post/" + post_id;
    const button = event.target;
    const headers = new Headers({
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()
    })

    if (button.id == "update") {
      const payload = {
        content: document.querySelector("textarea").value,
        exist: document.getElementsByName("exist")[0].checked
      }
      fetch(url, {
        method: "PUT",
        body: JSON.stringify(payload),
        headers: headers,
      }).then(res => res.json())
        .then(data => {
          let update_button = document.querySelector("#update");
          buttonSuccess(update_button)
        });
    } else if (button.id == "delete") {
      fetch(url, {
        method: "DELETE",
        headers: headers,
      }).then(res => res.json())
        .then(data => {
          let delete_button = document.querySelector("#delete");
          document.getElementsByName("exist")[0].checked = false
          buttonSuccess(delete_button)
        });
    }
  };
  document.querySelector("#form button#update").addEventListener("click", clickListener);
  document.querySelector("#form button#delete").addEventListener("click", clickListener);
  document.querySelector("#comment button").addEventListener("click", (event) => {
    const url = "/api/comment/" + post_id;
    fetch(url, {
      method: 'POST',
      body: JSON.stringify({
        author: document.querySelector("input[name=author]").value,
        content: document.querySelector("input[name=content]").value
      }),
      headers: new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      })
    }).then(res => res.json())
      .then(data => {
        if (data.success == true) {
          let button = document.querySelector("#comment button");
          buttonSuccess(button);
        }
      })
  });
})();
