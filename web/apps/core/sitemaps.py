"""Sitemap classes for every public URL on the site."""
from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.roles.models import TIER_ORDER, Category, Role


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return [
            "core:home",
            "roles:ranking",
            "roles:category_index",
            "core:sources",
            "core:limitations",
            "core:data_policy",
            "core:about",
            "core:compare",
            "reports:report",
            "reports:insights",
            "reports:methodology",
        ]

    def location(self, item: str) -> str:
        return reverse(item)


class RoleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    limit = 1000

    def items(self):
        return Role.objects.order_by("-score")

    def lastmod(self, obj: Role):
        return obj.last_updated

    def location(self, obj: Role) -> str:
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.order_by("name")

    def location(self, obj: Category) -> str:
        return obj.get_absolute_url()


class TierSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return list(TIER_ORDER)

    def location(self, item: str) -> str:
        return reverse("roles:tier", kwargs={"tier": item})


SITEMAPS = {
    "static": StaticSitemap,
    "roles": RoleSitemap,
    "categories": CategorySitemap,
    "tiers": TierSitemap,
}
