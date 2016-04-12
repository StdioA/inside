import time
import json
import tempfile
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.shortcuts import render
from .models import Post, Comment

def __get_post_data(post):
    result = {
            "id": post.id,
            "content": post.content.encode("utf-8"),
            "pub_date": int(time.mktime(post.pub_date.timetuple())),
            "comments": []
        }
    for comment in post.comment_set.all():
        result["comments"].append(comment.get_obj())

    return result


def import_data(request):
    if not request.user.is_superuser:
        raise Http404
    pass


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

    return render(request, "mblog/data.html")
