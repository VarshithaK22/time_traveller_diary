from django.urls import path
from . import views, entry_views, weather_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="/",
            http_method_names=["get", "post"],
            #   template_name='logout.html'
        ),
        name="logout",
    ),
    path("profile/", views.profile, name="profile"),
    path("", views.EntryListView.as_view(), name="home"),
    path("new/", entry_views.EntryCreateView.as_view(), name="entry_create"),
    path("<int:pk>/", entry_views.EntryDetailView.as_view(), name="entry_detail"),
    path("<int:pk>/update", entry_views.EntryUpdateView.as_view(), name="entry_update"),
    path("<int:pk>/delete", entry_views.EntryDeleteView.as_view(), name="entry_delete"),
    path(
        "random-adventure/",
        entry_views.RandomeAdventureView.as_view(),
        name="random_adventure",
    ),
    path(
        "fake-weather/",
        weather_view.RandomeWeatherView.as_view(),
        name="random_weather",
    ),
]
