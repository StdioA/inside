import json
from django.http import JsonResponse
from mblog.models import Post, Comment
from api.utils import LoginRequiredMixin
from django.views import View


class CommentView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id, exist=True)
        except Post.DoesNotExist:
            return JsonResponse({
                "success": False,
                "reason": "Post does not exist"
            }, status=404)

        result = {
            "success": True,
            "id": post_id,
            "comments": []
        }
        for comment in post.comment_set.all():
            result["comments"].append(comment.serialize())
        return JsonResponse(result)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id, exist=True)
        except Post.DoesNotExist:
            return JsonResponse({
                "success": False,
                "reason": "Post does not exist"
            }, status=404)

        comment = Comment(post=post,
                          author=request.POST["author"],
                          content=request.POST["content"])
        comment.save()
        return JsonResponse({"success": True})


class PostView(LoginRequiredMixin, View):
    permission_dict = {
        "post": "mblog.change_post",
        "put": "mblog.change_post"
    }

    def get(self, request, post_id):
        pk = post_id
        post = Post.objects.get(pk=pk, exist=True)

        previous_post = Post.objects.filter(
            pk__lt=pk, exist=True).order_by("-pk").first()
        previous_post_id = previous_post.id if previous_post else 0
        next_post = Post.objects.filter(pk__gt=pk, exist=True).first()
        next_post_id = next_post.id if next_post else 0

        result = {
            "success": True,
            "previous_id": previous_post_id,
            "next_id": next_post_id,
            "post": post.serialize()
        }
        return JsonResponse(result)

    def put(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        payload = json.loads(request.body)
        post.content = payload["content"]
        post.exist = payload["exist"]
        post.save()
        return JsonResponse({"success": True})

    def delete(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.exist = False
        post.save()
        return JsonResponse({"success": True})


class ArchiveView(LoginRequiredMixin, View):
    """
    /api/archive/9/counts/2
    从第9个开始倒数2个
    """
    def get(self, request, post_id, number):
        data = {
            "success": True,
        }
        if not number:
            number = 6
        else:
            number = int(number)

        query = {
            "exist": True
        }
        if post_id:
            query["pk__lte"] = post_id
        posts = Post.objects.filter(**query).order_by("-pk")[0:number]
        data["posts"] = [p.serialize() for p in posts]
        return JsonResponse(data)
