from django.urls import path

from . import views

app_name = "roles"

urlpatterns = [
    path("", views.ranking, name="ranking"),
    path("table/", views.ranking_table, name="ranking_table"),
    path("categories/", views.category_index, name="category_index"),
    path("categories/<slug:slug>/", views.category_detail, name="category"),
    path("tier/<str:tier>/", views.tier_detail, name="tier"),
    path("<slug:slug>/", views.role_detail, name="detail"),
]
