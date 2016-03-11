from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Post, Comment
from .settings import verify_password

# Create your views here.
def index(request):
    post = Post.objects.filter(exist=True).order_by("pk").last()
    return HttpResponseRedirect(reverse('mblog:post', kwargs={"pk": post.id}))

class PostView(generic.DetailView):
    model = Post
    template_name = "mblog/post.html"

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        pk = self.object.id;
        try:
            previous_post_id = Post.objects.filter(pk__lt=pk, exist=True).order_by("-pk")[0].id
        except (Post.DoesNotExist, IndexError):
            previous_post_id = 0
        try:
            next_post_id = Post.objects.filter(pk__gt=pk, exist=True)[0].id
        except (Post.DoesNotExist, IndexError):
            next_post_id = 0

        context["previous"] = previous_post_id
        context["current"] = pk
        context["next"] = next_post_id
        return context

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

def verify(request):
    return Http404()
