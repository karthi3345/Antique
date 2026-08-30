"""House app — The House, Chronicles, Private Acquisition, Contact."""
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET

from collection.models import Chronicle


@require_GET
def the_house(request):
    return render(request, "house/the-house.html")


@require_GET
def chronicles(request):
    articles = Chronicle.objects.all()
    return render(request, "house/chronicles.html", {"articles": articles})


@require_GET
def chronicle_detail(request, slug):
    article = get_object_or_404(Chronicle, slug=slug)
    return render(request, "house/chronicle.html", {"article": article})


@require_GET
@ensure_csrf_cookie
def acquisition(request):
    return render(request, "house/acquisition.html")


@require_GET
@ensure_csrf_cookie
def contact(request):
    return render(request, "house/contact.html")
