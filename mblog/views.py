from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Post, Comment
from .settings import verify_password

# Create your views here.
def index(request):
    post = Post.objects.filter(exist=True).order_by("pk").last()
    print Post.objects.all()
    return HttpResponseRedirect(reverse('mblog:post', kwargs={"pk": post.id}))

class PostView(generic.DetailView):
    model = Post
    template_name = "mblog/post.html"

def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        comment = Comment(post=post, 
                          author=request.POST["author"],
                          content=request.POST["content"])
        comment.save()
        return HttpResponseRedirect(reverse('mblog:post', kwargs={"pk": post_id}))
    else:
        return Http404()

def verify(request):
    return Http404()
