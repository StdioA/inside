import datetime
import time
import json
import tempfile
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.shortcuts import render
from mblog.models import Post, Comment

def __get_post_data(post):
    result = {
            "id": post.id,
            "content": post.content.encode("utf-8"),
            "pub_date": int(time.mktime(post.pub_date.timetuple())),
            "exist": post.exist,
            "comments": []
        }
    for comment in post.comment_set.all():
        result["comments"].append(comment.get_obj())

    return result


def import_data(request):
    if not request.user.is_superuser:
        raise Http404
    
    content = {}
    if request.method == "POST":
        data_file = request.FILES.get("data", None)
        if not data_file:
            content["success"] = False
            content["message"] = "Please Select data file."
            return render(request, "backstage/data-upload-result.html", content)

        data_str = data_file.read()

        try:
            posts = json.loads(data_str)["posts"]
        except ValueError:
            content["success"] = False
            content["message"] = "JSON Parsing Error"
            return render(request, "backstage/data-upload-result.html", content)

        posts.sort(key=lambda o: o["pub_date"])

        for p in posts:
            pub_date = datetime.datetime.fromtimestamp(p["pub_date"])
            post = Post(content=p["content"], pub_date=pub_date, exist=p["exist"])
            post.save()

            for c in p["comments"]:
                comment = Comment(post=post, author=c["author"], content=c["content"])
                comment.save()

        content["success"] = True
        content["message"] = "%d posts has been imported!"%len(posts)
        return render(request, "backstage/data-upload-result.html", content)

    elif request.method == "GET":
        content["success"] = False
        content["message"] = "Import the posts"
        return render(request, "mblog/data-upload-result.html", content)


def export_data(request):
    if not request.user.is_superuser:
        raise Http404

    data = {}
    data["posts"] = [__get_post_data(post) for post in Post.objects.all()]
    datas = json.dumps(data)

    f = tempfile.SpooledTemporaryFile(mode="wb")
    f.write(datas)
    f.seek(0)

    response = FileResponse(f)
    response["Content-Type"] = "application/octet-stream"
    return response


def data(request):
    if not request.user.is_superuser:
        raise Http404

    return render(request, "backstage/data.html")
