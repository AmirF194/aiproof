from django.contrib import admin

from .models import Category, Role, RoleMetric, TierSummary


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "n_roles", "avg_score")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("rank", "role", "category", "score", "tier", "demand_trend")
    list_filter = ("tier", "category", "demand_trend")
    search_fields = ("role", "category__name")
    prepopulated_fields = {"slug": ("role",)}
    list_select_related = ("category",)


@admin.register(RoleMetric)
class RoleMetricAdmin(admin.ModelAdmin):
    list_display = ("role", "postings_2026_current", "postings_yoy_pct", "ai_mention_pct_2026")
    search_fields = ("role__role",)


@admin.register(TierSummary)
class TierSummaryAdmin(admin.ModelAdmin):
    list_display = ("tier", "n_roles", "avg_score")
