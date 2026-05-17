from django.db import models
from django.urls import reverse
from django.utils.text import slugify


TIER_FORTRESS = "fortress"
TIER_SAFE = "safe"
TIER_STABLE = "stable"
TIER_EXPOSED = "exposed"
TIER_AT_RISK = "at_risk"

TIER_ORDER = [TIER_FORTRESS, TIER_SAFE, TIER_STABLE, TIER_EXPOSED, TIER_AT_RISK]

TIER_LABELS = {
    TIER_FORTRESS: "Fortress",
    TIER_SAFE: "Safe",
    TIER_STABLE: "Stable",
    TIER_EXPOSED: "Exposed",
    TIER_AT_RISK: "At risk",
}

TIER_BLURBS = {
    TIER_FORTRESS: "Build a career here without hedging.",
    TIER_SAFE: "Senior path is durable. Junior path is harder than 2020.",
    TIER_STABLE: "Specialize or get exposed. Generalist track compresses.",
    TIER_EXPOSED: "Plan an adjacent move within 2-3 years.",
    TIER_AT_RISK: "Plan a transition. Headcount shrinks every year.",
}

TIER_COLORS = {
    TIER_FORTRESS: "emerald",
    TIER_SAFE: "sky",
    TIER_STABLE: "amber",
    TIER_EXPOSED: "orange",
    TIER_AT_RISK: "rose",
}


TREND_RISING = "rising"
TREND_FLAT = "flat"
TREND_DECLINING = "declining"

TREND_LABELS = {
    TREND_RISING: "Rising",
    TREND_FLAT: "Flat",
    TREND_DECLINING: "Declining",
}


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    rationale = models.TextField(blank=True)

    n_roles = models.PositiveIntegerField(default=0)
    avg_score = models.FloatField(default=0)
    avg_demand = models.FloatField(default=0)
    avg_automation_resistance = models.FloatField(default=0)
    avg_skill_depth = models.FloatField(default=0)
    avg_strategic_importance = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["-avg_score", "name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("roles:category", kwargs={"slug": self.slug})


class Role(models.Model):
    TIER_CHOICES = [(k, TIER_LABELS[k]) for k in TIER_ORDER]
    TREND_CHOICES = [
        (TREND_RISING, "Rising"),
        (TREND_FLAT, "Flat"),
        (TREND_DECLINING, "Declining"),
    ]

    role = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="roles"
    )

    demand = models.PositiveSmallIntegerField()
    automation_resistance = models.PositiveSmallIntegerField()
    skill_depth = models.PositiveSmallIntegerField()
    strategic_importance = models.PositiveSmallIntegerField()

    score = models.PositiveSmallIntegerField(db_index=True)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, db_index=True)
    demand_trend = models.CharField(
        max_length=20, choices=TREND_CHOICES, db_index=True
    )

    salary_low_usd = models.PositiveIntegerField(null=True, blank=True)
    salary_high_usd = models.PositiveIntegerField(null=True, blank=True)

    rank = models.PositiveIntegerField(db_index=True, default=0)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-score", "role"]
        constraints = [
            models.UniqueConstraint(
                fields=["role", "category"], name="unique_role_per_category"
            ),
        ]

    def __str__(self) -> str:
        return self.role

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.role)[:200] or "role"
            slug = base
            n = 2
            while Role.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("roles:detail", kwargs={"slug": self.slug})

    @property
    def tier_label(self) -> str:
        return TIER_LABELS.get(self.tier, self.tier)

    @property
    def tier_color(self) -> str:
        return TIER_COLORS.get(self.tier, "slate")

    @property
    def trend_label(self) -> str:
        return TREND_LABELS.get(self.demand_trend, self.demand_trend)

    @property
    def salary_range_display(self) -> str:
        if self.salary_low_usd and self.salary_high_usd:
            return f"${self.salary_low_usd // 1000}k - ${self.salary_high_usd // 1000}k"
        return "-"


class RoleMetric(models.Model):
    role = models.OneToOneField(
        Role, on_delete=models.CASCADE, related_name="metrics"
    )
    postings_2024_baseline = models.PositiveIntegerField(null=True, blank=True)
    postings_2025_jan = models.PositiveIntegerField(null=True, blank=True)
    postings_2026_current = models.PositiveIntegerField(null=True, blank=True)
    postings_yoy_pct = models.FloatField(null=True, blank=True)
    postings_2yr_pct = models.FloatField(null=True, blank=True)
    ai_mention_pct_2026 = models.FloatField(null=True, blank=True)
    ai_mention_delta_pp = models.FloatField(null=True, blank=True)
    copilot_mention_pct_2026 = models.FloatField(null=True, blank=True)
    trend_direction = models.CharField(max_length=40, blank=True)

    def __str__(self) -> str:
        return f"metrics for {self.role.role}"


class TierSummary(models.Model):
    tier = models.CharField(max_length=20, unique=True)
    n_roles = models.PositiveIntegerField(default=0)
    avg_score = models.FloatField(default=0)
    avg_demand = models.FloatField(default=0)
    avg_automation_resistance = models.FloatField(default=0)
    avg_skill_depth = models.FloatField(default=0)
    avg_strategic_importance = models.FloatField(default=0)

    class Meta:
        ordering = ["-avg_score"]

    def __str__(self) -> str:
        return self.tier
