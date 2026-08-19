"""End-to-end smoke tests — every public URL renders 200 with valid markup.

These run in CI before deploy. The fixtures are minimal — one Category and
two Roles — enough to exercise the templates without depending on the
full 1,000-role load.
"""
from __future__ import annotations

import pytest
from django.urls import reverse

from apps.roles.models import Category, Role, RoleMetric


@pytest.fixture
def base_data(db):
    cat = Category.objects.create(name="Engineering", slug="engineering")
    Category.objects.create(name="Data & AI", slug="data-ai")
    r1 = Role.objects.create(
        role="Solutions Architect",
        slug="solutions-architect",
        category=cat,
        demand=8, automation_resistance=8, skill_depth=8, strategic_importance=8,
        score=80, tier="safe", demand_trend="rising",
        salary_low_usd=180_000, salary_high_usd=350_000,
        rank=1,
        notes="Owns architectural decisions across teams.",
        seniority_level="Senior", role_family="Cloud",
        human_judgment_score=8, stakeholder_interaction_score=7,
        physical_world_dependency_score=2, ai_augmentation_potential_score=5,
        regulatory_relevance_score=6, confidence_score=70,
        why_ai_resistant="Strong on automation resistance.",
        why_ai_exposed="",
    )
    Role.objects.create(
        role="QA Manual",
        slug="qa-manual",
        category=cat,
        demand=3, automation_resistance=2, skill_depth=2, strategic_importance=2,
        score=20, tier="at_risk", demand_trend="declining",
        salary_low_usd=40_000, salary_high_usd=80_000,
        rank=1000,
        notes="Manual testing role.",
        seniority_level="Mid", role_family="QA & Testing",
        human_judgment_score=2, stakeholder_interaction_score=3,
        physical_world_dependency_score=2, ai_augmentation_potential_score=6,
        regulatory_relevance_score=3, confidence_score=50,
        why_ai_resistant="",
        why_ai_exposed="Low on every base axis.",
    )
    RoleMetric.objects.create(role=r1, postings_2026_current=100, ai_mention_pct_2026=10.0)
    return cat, r1


@pytest.mark.parametrize("url_name", [
    "core:home",
    "core:about",
    "core:sources",
    "core:limitations",
    "core:data_policy",
    "core:compare",
    "roles:ranking",
    "roles:ranking_table",
    "roles:category_index",
])
def test_public_urls_render(client, base_data, url_name):
    response = client.get(reverse(url_name))
    assert response.status_code == 200, f"{url_name} returned {response.status_code}"


def test_role_detail(client, base_data):
    response = client.get(reverse("roles:detail", kwargs={"slug": "solutions-architect"}))
    assert response.status_code == 200
    body = response.content.decode()
    assert "Solutions Architect" in body
    assert "Score breakdown" in body
    assert "Confidence" in body


def test_compare_view(client, base_data):
    response = client.get("/compare/?roles=solutions-architect,qa-manual")
    assert response.status_code == 200
    body = response.content.decode()
    assert "Solutions Architect" in body
    assert "QA Manual" in body
    assert "Score dimension" in body


def test_sitemap_and_robots(client, base_data):
    sitemap = client.get("/sitemap.xml")
    assert sitemap.status_code == 200
    assert "solutions-architect" in sitemap.content.decode()

    robots = client.get("/robots.txt")
    assert robots.status_code == 200
    assert "Sitemap:" in robots.content.decode()


def test_filter_seniority_and_family(client, base_data):
    r = client.get("/roles/?seniority=Senior")
    assert r.status_code == 200
    assert "Solutions Architect" in r.content.decode()
    assert "QA Manual" not in r.content.decode()

    r = client.get("/roles/?family=QA%20%26%20Testing")
    assert r.status_code == 200
    body = r.content.decode()
    assert "QA Manual" in body
    assert "Solutions Architect" not in body


def test_limitations_coverage_is_computed_not_hardcoded(client, base_data):
    """The coverage figure on /limitations/ must come from the database.

    It was hard-coded at "141 of 1,000" for months while the crawlers grew to
    cover far more roles, so the page understated our own coverage by ~2x.
    """
    response = client.get(reverse("core:limitations"))
    assert response.status_code == 200
    # The template wraps this sentence across several source lines.
    body = " ".join(response.content.decode().split())

    # base_data has 2 roles, exactly one of which carries a live posting count.
    assert "1 of 2 roles have a live posting count" in body
    assert "The other 1 use the calibrated baseline" in body
    assert "141" not in body
