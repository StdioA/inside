from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    next_url = request.GET.dict().get("next", "/0")

    if request.method == "GET":
        return render(request, "mblog/login.html")
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if (user is not None) and user.is_active:
            login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            error_message = "Invalid username or password (╯3╰)"
            return render(request, "mblog/login.html", {
                    "error": error_message
                })
            # return HttpResponseRedirect(request.get_full_path())


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("mblog:index"))
