from django.urls import path
from . import views

urlpatterns = [
    path("chronicles/", views.chronicles, name="chronicles"),
    path("chronicles/<slug:slug>/", views.chronicle_detail, name="chronicle_detail"),
    path("acquisition/", views.acquisition, name="acquisition"),
    path("contact/", views.contact, name="contact"),
    path("the-house/", views.the_house, name="the_house"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
]
