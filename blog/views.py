from django.shortcuts import render
from . import models


def blog(request):
    context = {"posts": models.Post.objects.all().exclude(translated__isnull=True).order_by('-time')}
    if request.headers.get("HX-Request"):
        return render(request, "partials/blog_partial.html", context)
    return render(request, "includes/blog.html", context)
