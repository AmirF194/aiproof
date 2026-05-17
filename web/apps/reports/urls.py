from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.report, name="report"),
    path("insights/", views.insights, name="insights"),
    path("methodology/", views.methodology, name="methodology"),
]
