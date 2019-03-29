from django.http import HttpResponse


def serve_static(filename):
    with open(filename, encoding='utf-8') as f:
        return HttpResponse(f.read())
