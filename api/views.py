# coding: utf-8
# TODO: Build API using Django REST Framework

from django.http import JsonResponse
from mblog.models import Post, Comment
from api.utils import api_login_required




@api_login_required
def comment(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, exist=True)
    except Post.DoesNotExist:
        return JsonResponse({
            "success": False,
            "reason": "Post does not exist"
        }, status=404)

    if request.method == "GET":
        result = {
            "success": True,
            "id": post_id,
            "comments": []
        }
        for comment in post.comment_set.all():
            result["comments"].append(comment.serialize())
        return JsonResponse(result)
    elif request.method == "POST":
        comment = Comment(post=post,
                            author=request.POST["author"],
                            content=request.POST["content"])
        comment.save()
        return JsonResponse({"success": True})


@api_login_required
def post(request, post_id):
    if request.method == "GET":
        try:
            post = Post.objects.get(pk=post_id, exist=True)
        except Post.DoesNotExist:
            return JsonResponse({
                "success": False,
                "reason": "Post does not exist"
            }, status=404)

        pk = post_id
        try:
            previous_post_id = Post.objects.filter(
                pk__lt=pk, exist=True).order_by("-pk")[0].id
        except (Post.DoesNotExist, IndexError):
            previous_post_id = 0
        try:
            next_post_id = Post.objects.filter(pk__gt=pk, exist=True)[0].id
        except (Post.DoesNotExist, IndexError):
            next_post_id = 0

        result = {
            "success": True,
            "previous_id": previous_post_id,
            "next_id": next_post_id,
            "post": post.serialize()
        }
        return JsonResponse(result)

    elif request.method == "POST":                       # 更改POST
        if request.user.has_perm("mblog.change_post"):
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "reason": "Post does not exist"
                })

            post = Post.objects.get(pk=post_id)
            post.content = request.POST["content"]
            post.exist = (request.POST["exist"] == "true")
            post.save()
            return JsonResponse({"success": True})

        else:
            return JsonResponse({
                        "success": False,
                        "reason": "Unauthorized"
                    }, status=401)

    elif request.method == "DELETE":                     # 删除POST
        if request.user.has_perm("mblog.change_post"):
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "reason": "Post does not exist"
                })

            post = Post.objects.get(pk=post_id)
            post.exist = False
            post.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({
                        "success": False,
                        "reason": "Unauthorized"
                    }, status=401)


@api_login_required
def archive(request, post_id, number):
    """
    /api/archive/9/counts/2
    从第9个开始倒数2个
    """
    data = {
        "success": True,
    }
    if not number:
        number = 6
    else:
        number = int(number)

    if not post_id:
        posts = Post.objects.filter(exist=True).order_by("-pk")[0:number]
    else:
        posts = Post.objects.filter(pk__lte=post_id,
                                    exist=True).order_by("-pk")[0:number]

    data["posts"] = [p.serialize() for p in posts]

    return JsonResponse(data)
