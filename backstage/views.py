import datetime
import json
import tempfile
from operator import itemgetter
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.views import View
from mblog.models import Post, Comment


class DataImportView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {
            "success": False,
            "message": "Import the posts"
        }
        return render(request, "mblog/data-upload-result.html", content)

    def parse_request_data(self, request):
        data_file = request.FILES.get("data", None)
        if not data_file:
            raise ValueError("Please Select data file.")

        data_str = data_file.read()
        try:
            posts = json.loads(data_str)["posts"]
        except ValueError:
            raise ValueError("JSON Parsing Error")
        return posts

    def post(self, request):
        content = {
            "success": True
        }
        try:
            posts = self.parse_request_data(request)
        except ValueError as e:
            content.update({
                "success": False,
                "message": e.args[0]
            })

        if content["success"]:
            posts.sort(key=itemgetter("pub_date"))
            for p in posts:
                pub_date = datetime.datetime.fromtimestamp(p["pub_date"])
                post = Post.objects.create(
                    content=p["content"], pub_date=pub_date, exist=p["exist"])

                for c in p["comments"]:
                    comment = Comment(post=post, author=c["author"],
                                      content=c["content"])
                    comment.save()
            content["success"] = True
            content["message"] = "%d posts has been imported!" % len(posts)
        return render(request, "backstage/data-upload-result.html", content)


class DataExportView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        data = {}
        data["posts"] = [post.dump_payload for post in Post.objects.all()]
        json_data = json.dumps(data)
        f = tempfile.SpooledTemporaryFile(mode="wb")
        f.write(json_data.encode('utf-8'))
        f.seek(0)

        response = FileResponse(f)
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = ('attachment; filename='
                                           '\"inside-data.json\"')
        return response


def index(request):
    if not request.user.is_superuser:
        raise Http404

    return render(request, "backstage/data.html")
