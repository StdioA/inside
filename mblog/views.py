from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .settings import verify_password

# Create your views here.
def index(request):
    post = Post.objects.filter(exist=True).order_by("pk").last()
    return HttpResponseRedirect(reverse('mblog:post', kwargs={"pk": post.id}))


def view_post(request, pk):
    with file("mblog/static/mblog/html/post.html", "r") as f:
        return HttpResponse(f.read())


def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        author, content = request.POST["author"], request.POST["content"]
        if author and content:
            comment = Comment(post=post, 
                              author=request.POST["author"],
                              content=request.POST["content"])
            comment.save()
        return HttpResponseRedirect(reverse('mblog:post', kwargs={"pk": post_id}))
    else:
        return Http404()


@login_required
def manage_post(request):
    return render(request, "mblog/manage.html")
