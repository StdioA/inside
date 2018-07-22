import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Post, Comment


@login_required
def index(request):
    post = Post.objects.filter(exist=True).order_by("pk").last()
    if post:
        return HttpResponseRedirect(reverse('mblog:post', kwargs={"pk": post.id}))
    else:
        raise Http404

@login_required
def view_post(request, pk):
    if request.user.has_perm("mblog.change_post"):
        post = get_object_or_404(Post, pk=pk)
        pk = post.id

        try:
            previous_post_id = Post.objects.filter(pk__lt=pk).order_by("-pk")[0].id
        except (Post.DoesNotExist, IndexError):
            previous_post_id = 0
        try:
            next_post_id = Post.objects.filter(pk__gt=pk)[0].id
        except (Post.DoesNotExist, IndexError):
            next_post_id = 0

        context = {
                    "post":post,
                    "previous": previous_post_id,
                    "next": next_post_id
                }
        return render(request, "mblog/edit.html", context)

    else:
        with open("mblog/static/mblog/html/post.html", "r", encoding='utf-8') as f:
            return HttpResponse(f.read())

@login_required
def archive(request):
    with open("mblog/static/mblog/html/archive.html", "r", encoding='utf-8') as f:
        return HttpResponse(f.read())

@login_required
def add_post(request):
    if request.method == "GET":
        return render(request, "mblog/new.html")
    elif request.method == "POST":
        post = Post(content=request.POST["content"])
        post.save()
        return HttpResponseRedirect(reverse('mblog:post', kwargs={"pk": post.id}))
