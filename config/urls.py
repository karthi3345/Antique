"""Volgo URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.decorators.csrf import ensure_csrf_cookie

from collection import views as collection_views
from house import views as house_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ensure_csrf_cookie(collection_views.home), name="home"),
    path("collection/", collection_views.collection_view, name="collection"),
    path("objects/<int:number>/", ensure_csrf_cookie(collection_views.artifact_detail), name="artifact_detail"),
    path("api/objects/", collection_views.api_objects, name="api_objects"),
    path("api/objects/<int:number>/", collection_views.api_artifact, name="api_artifact"),
    path("api/enquiry/", collection_views.api_enquiry, name="api_enquiry"),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "img/favicon.svg", permanent=False)),
    path("", include("house.urls")),
]
