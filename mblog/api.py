from django.http import JsonResponse
from .models import Post, Comment

def comment(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, exist=True)
    except Post.DoesNotExist:
        return JsonResponse({"success": False, "reason": "Post not exist"})

    if request.method == "GET":
        result = {
            "success": True,
            "id": post_id,
            "comments": []
        }
        for comment in post.comment_set.all():
            result["comments"].append(comment.getObj())
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
        return JsonResponse({"success": False, "reason": "Post not exist"})

    if request.method == "GET":
        result = {
            "success": True,
            "id": post_id,
            "content": post.content.encode("utf-8"),
            "pub_date": post.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
            "comments": []
        }
        for comment in post.comment_set.all():
            result["comments"].append(comment.getObj())

        return JsonResponse(result)
