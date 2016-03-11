from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

def user_login(request):
    if request.method == "GET":
        return render(request, "mblog/login.html")
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("mblog:manage"))
        else:
            return render(request, "mblog/login.html")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("mblog:index"))
