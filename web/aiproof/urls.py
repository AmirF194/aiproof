from django.contrib import admin
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "favicon.ico",
        RedirectView.as_view(url=static("favicon.ico"), permanent=True),
    ),
    path("", include("apps.core.urls")),
    path("roles/", include("apps.roles.urls")),
    path("report/", include("apps.reports.urls")),
]
