from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("sources/", views.sources, name="sources"),
    path("data/<str:filename>", views.data_download, name="data_download"),
]
