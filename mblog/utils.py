from django.http import HttpResponse


def serve_static(filename):
    with open(filename) as f:
        return HttpResponse(f.read())
