"""House app ?" The House, Chronicles, Private Acquisition, Contact, Auth."""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout

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

@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "house/register.html", {"form": form})

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, "house/login.html", {"form": form})

@require_http_methods(["GET", "POST"])
def logout_view(request):
    auth_logout(request)
    return redirect("home")

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    if request.method == "POST":
        # Handle basic user updates
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        return redirect('profile')
        
    return render(request, "house/profile.html")
