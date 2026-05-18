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
