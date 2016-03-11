# coding: utf-8
# TODO: Build API using Django REST Framework

from django.http import JsonResponse
from .models import Post, Comment

def comment(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, exist=True)
    except Post.DoesNotExist:
        return JsonResponse({"success": False, "reason": "Post does not exist"})

    if request.method == "GET":
        result = {
            "success": True,
            "id": post_id,
            "comments": []
        }
        for comment in post.comment_set.all():
            result["comments"].append(comment.get_obj())
        return JsonResponse(result)
    elif request.method == "POST":
        comment = Comment(post=post, 
                          author=request.POST["author"],
                          content=request.POST["content"])
        comment.save()
        return JsonResponse({"success": True})

def post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, exist=True)
    except Post.DoesNotExist:
        return JsonResponse({"success": False, "reason": "Post does not exist"})

    if request.method == "GET":
        pk = post_id
        try:
            previous_post_id = Post.objects.filter(pk__lt=pk, exist=True).order_by("-pk")[0].id
        except (Post.DoesNotExist, IndexError):
            previous_post_id = 0
        try:
            next_post_id = Post.objects.filter(pk__gt=pk, exist=True)[0].id
        except (Post.DoesNotExist, IndexError):
            next_post_id = 0

        result = {
            "success": True,
            "id": post_id,
            "previous_id": previous_post_id,
            "next_id": next_post_id,
            "content": post.content.encode("utf-8"),
            "pub_date": post.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
            "comments": []
        }
        for comment in post.comment_set.all():
            result["comments"].append(comment.get_obj())

        return JsonResponse(result)
    elif request.method == "PUT":       # 发布新的post
        pass
