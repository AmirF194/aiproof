"""Pure-function tests for apps.roles.scoring."""
from __future__ import annotations

import pytest

from apps.roles import scoring


@pytest.mark.parametrize("title,expected", [
    ("Chief AI Officer", "C-suite"),
    ("CTO", "C-suite"),
    ("VP of Engineering", "VP"),
    ("Director of Data", "Director"),
    ("Head of Backend", "Director"),
    ("Principal Engineer", "Principal"),
    ("Distinguished Engineer", "Principal"),
    ("Staff Engineer", "Staff"),
    ("Senior Backend Engineer", "Senior"),
    ("Sr. Data Scientist", "Senior"),
    ("Lead Designer", "Lead"),
    ("Junior Frontend Engineer", "Junior"),
    ("Backend Engineer", "Mid"),
    ("Solutions Architect", "Mid"),
])
def test_parse_seniority(title, expected):
    assert scoring.parse_seniority(title) == expected


@pytest.mark.parametrize("title,category,expected_family", [
    ("Senior LLM Engineer", "Data & AI", "AI & ML"),
    ("Backend Engineer", "Engineering", "Backend"),
    ("Frontend Engineer", "Engineering", "Frontend"),
    ("iOS Developer", "Engineering", "Mobile"),
    ("SRE", "Platform & Infrastructure", "DevOps & SRE"),
    ("Security Engineer", "Security", "Security"),
    ("Product Manager", "Product & Design", "Product"),
    ("UX Researcher", "Product & Design", "Design"),
    ("Hardware Engineer", "Specialized & Emerging", "Hardware"),
    ("Game Programmer", "Specialized & Emerging", "Game"),
    ("Blockchain Developer", "Specialized & Emerging", "Blockchain"),
    # Fallback to category when no pattern matches:
    ("Some Niche Role", "Engineering", "Engineering"),
])
def test_derive_role_family(title, category, expected_family):
    assert scoring.derive_role_family(title, category) == expected_family


def test_human_judgment_is_weighted_blend():
    # HJ = 0.6*AR + 0.4*SD, rounded.
    assert scoring.human_judgment_score(10, 10) == 10
    assert scoring.human_judgment_score(0, 0) == 0
    assert scoring.human_judgment_score(5, 5) == 5
    assert scoring.human_judgment_score(10, 0) == 6
    assert scoring.human_judgment_score(0, 10) == 4


def test_ai_augmentation_complements_resistance():
    # Roles with low resistance + high skill score highest on augmentation.
    high = scoring.ai_augmentation_potential_score(automation_resistance=2, skill_depth=10)
    low  = scoring.ai_augmentation_potential_score(automation_resistance=10, skill_depth=2)
    assert high > low
    # All outputs bounded.
    for ar in range(0, 11):
        for sd in range(0, 11):
            v = scoring.ai_augmentation_potential_score(ar, sd)
            assert 0 <= v <= 10


def test_physical_dependency_lifts_for_hardware():
    base = scoring.physical_world_dependency_score("Backend Engineer", "Engineering")
    hard = scoring.physical_world_dependency_score("Hardware Engineer", "Engineering")
    assert hard > base


def test_confidence_caps_at_100():
    full = scoring.confidence_score(scoring.ConfidenceInputs(
        has_live_postings=True, is_calibrated=True,
        has_salary_band=True, has_description=True,
    ))
    assert full == 100
    minimal = scoring.confidence_score(scoring.ConfidenceInputs(
        has_live_postings=False, is_calibrated=False,
        has_salary_band=False, has_description=False,
    ))
    assert minimal == 40


def test_why_resistant_silent_when_no_axis_above_threshold():
    # Everything below 6/10 → empty string.
    blurb = scoring.why_ai_resistant({
        "automation_resistance": 5,
        "skill_depth": 5,
        "strategic_importance": 5,
        "human_judgment": 5,
        "stakeholder_interaction": 5,
    })
    assert blurb == ""


def test_why_resistant_picks_top_two():
    blurb = scoring.why_ai_resistant({
        "automation_resistance": 10,
        "skill_depth": 9,
        "strategic_importance": 2,
        "human_judgment": 2,
        "stakeholder_interaction": 2,
    })
    assert "automation resistance (10/10)" in blurb
    assert "skill depth (9/10)" in blurb


# --- Role enrichment templates ------------------------------------------

def test_role_overview_prefers_family_over_category():
    # Backend has its own entry — should be picked over generic Engineering.
    backend = scoring.role_overview("Backend", "Engineering", "Senior")
    engineering = scoring.role_overview("Engineering", "Engineering", "Senior")
    assert "Backend engineers" in backend
    assert backend != engineering


def test_role_overview_falls_back_to_category_then_engineering():
    # Unknown family + known category → category entry wins.
    out = scoring.role_overview("NotAFamily", "Engineering Leadership", "Director")
    assert "leadership" in out.lower()
    # Unknown family + unknown category → Engineering fallback (never empty).
    fallback = scoring.role_overview("", "", "Mid")
    assert fallback
    assert "engineers" in fallback.lower()


def test_role_overview_appends_seniority_scope():
    out_junior = scoring.role_overview("Backend", "Engineering", "Junior")
    out_staff = scoring.role_overview("Backend", "Engineering", "Staff")
    assert "Junior" in out_junior
    assert "Staff" in out_staff
    assert out_junior != out_staff


def test_role_responsibilities_returns_a_list_with_content():
    items = scoring.role_responsibilities("Backend", "Engineering")
    assert isinstance(items, list)
    assert len(items) >= 4
    assert all(isinstance(s, str) and s.strip() for s in items)


def test_role_responsibilities_returns_a_fresh_list():
    # Should not mutate the internal dict if a caller modifies the result.
    a = scoring.role_responsibilities("Backend", "Engineering")
    a.append("test mutation")
    b = scoring.role_responsibilities("Backend", "Engineering")
    assert "test mutation" not in b


def test_role_typical_tools_returns_list_with_content():
    tools = scoring.role_typical_tools("Frontend", "Engineering")
    assert "TypeScript" in tools
    assert len(tools) >= 4


def test_role_day_to_day_and_ai_impact_are_nonempty():
    assert scoring.role_day_to_day("Backend", "Engineering")
    assert scoring.role_ai_impact("Backend", "Engineering")
    # Even on full fallback (no family, no category match), we still get content.
    assert scoring.role_day_to_day("", "")
    assert scoring.role_ai_impact("", "")


@pytest.mark.parametrize("family", [
    "Backend", "Frontend", "Mobile", "AI & ML", "Data", "Security",
    "DevOps & SRE", "Cloud", "QA & Testing", "Product", "Design",
    "Hardware", "Game", "Blockchain",
])
def test_all_families_have_complete_enrichment(family):
    """Every family declared in _FAMILY_PATTERNS must have all five enrichment fields."""
    assert scoring.role_overview(family, "Engineering", "Mid")
    assert scoring.role_responsibilities(family, "Engineering")
    assert scoring.role_typical_tools(family, "Engineering")
    assert scoring.role_day_to_day(family, "Engineering")
    assert scoring.role_ai_impact(family, "Engineering")


@pytest.mark.parametrize("category", [
    "Engineering", "Engineering Leadership", "Data & AI",
    "Platform & Infrastructure", "Product & Design", "Quality & Testing",
    "Security", "Specialized & Emerging",
])
def test_all_categories_have_complete_enrichment(category):
    """Every category in the dataset must have a fallback enrichment entry."""
    assert scoring.role_overview("", category, "Mid")
    assert scoring.role_responsibilities("", category)
    assert scoring.role_typical_tools("", category)
    assert scoring.role_day_to_day("", category)
    assert scoring.role_ai_impact("", category)


def test_role_overview_is_deterministic():
    """Same inputs → same outputs across calls (Rule #2 invariant)."""
    a = scoring.role_overview("Backend", "Engineering", "Senior")
    b = scoring.role_overview("Backend", "Engineering", "Senior")
    assert a == b
