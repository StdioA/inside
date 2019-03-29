from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from mblog.models import Post
from mblog.utils import serve_static


@login_required
def index(request):
    post = Post.objects.filter(exist=True).order_by("pk").last()
    if post:
        return HttpResponseRedirect(
            reverse('mblog:post', kwargs={"pk": post.id}))
    else:
        raise Http404


@login_required
def view_post(request, pk):
    if request.user.has_perm("mblog.change_post"):
        post = get_object_or_404(Post, pk=pk)

        previous_post = Post.objects.filter(pk__lt=pk).order_by("-pk").first()
        previous_post_id = previous_post.id if previous_post else 0
        next_post = Post.objects.filter(pk__gt=pk).first()
        next_post_id = next_post.id if next_post else 0

        context = {
            "post": post,
            "previous": previous_post_id,
            "next": next_post_id
        }
        return render(request, "mblog/edit.html", context)
    else:
        return serve_static("mblog/static/mblog/html/post.html")


@login_required
def archive(request):
    return serve_static("mblog/static/mblog/html/archive.html")


@login_required
def add_post(request):
    if request.method == "GET":
        return render(request, "mblog/new.html")
    elif request.method == "POST":
        post = Post(content=request.POST["content"])
        post.save()
        return HttpResponseRedirect(
            reverse('mblog:post', kwargs={"pk": post.id}))
