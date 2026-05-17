from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("roles/", include("apps.roles.urls")),
    path("report/", include("apps.reports.urls")),
]
