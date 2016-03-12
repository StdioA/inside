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

    elif request.method == "POST":                       # 更改POST
        if request.user.is_authenticated():
            post = Post.objects.get(pk=post_id)
            post.content = request.POST["content"]
            post.save()
            return JsonResponse({"success": True})

        else:
            return JsonResponse({
                        "success": False,
                        "reason": "Login Required"
                    })
            
    elif request.method == "DELETE":                     # 删除POST
        if request.user.is_authenticated():
            post = Post.objects.get(pk=post_id)
            post.exist = False
            post.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({
                        "success": False,
                        "reason": "Login Required"
                    })            

def __get_post_data(post):
    result = {
            "id": post.id,
            "content": post.content.encode("utf-8"),
            "pub_date": post.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
            "comments": []
        }
    for comment in post.comment_set.all():
        result["comments"].append(comment.get_obj())

    return result


def archive(request, post_id, number):
    """
    /api/archive/9/counts/2
    从第9个开始倒数2个
    """
    data = {
        "success": True,
        "posts": []
    }
    if not number:
        number = 6

    if not post_id:
        posts = Post.objects.filter(exist=True).order_by("-pk")[0:number]
    else:
        posts = Post.objects.filter(pk__lte=post_id,
                                    exist=True).order_by("-pk")[0:number]

    for post in posts:
        data["posts"].append(__get_post_data(post))

    return JsonResponse(data)


def get_latest(request):
    post_id = Post.objects.filter(exist=True).order_by("-pk").first().id;
    return JsonResponse({
            "latest": post_id
        })
