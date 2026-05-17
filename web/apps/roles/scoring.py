"""Deterministic scoring formulas for the extended role schema.

Pure functions over the existing 4 base axes (demand, automation_resistance,
skill_depth, strategic_importance) plus the role name and category. No
network calls, no randomness, no LLM. The output of every function in this
module is reproducible from the inputs.

The formulas are published in /report/methodology/ — when you change a
formula here, also update the methodology page so users can audit the math.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


# --- Category coefficients ------------------------------------------------
# Per-category multipliers for the four derived dimensions. Set conservatively
# so the median role sits near 5/10 on each dimension.
CATEGORY_COEFFS: dict[str, dict[str, float]] = {
    "Engineering Leadership":   {"stakeholder": 1.4, "regulatory": 1.2, "physical": 0.4, "augment": 0.7},
    "Security":                 {"stakeholder": 1.0, "regulatory": 1.5, "physical": 0.7, "augment": 0.8},
    "Data & AI":                {"stakeholder": 0.9, "regulatory": 1.0, "physical": 0.3, "augment": 1.3},
    "Platform & Infrastructure":{"stakeholder": 0.8, "regulatory": 0.9, "physical": 0.6, "augment": 1.0},
    "Engineering":              {"stakeholder": 0.7, "regulatory": 0.6, "physical": 0.3, "augment": 1.1},
    "Specialized & Emerging":   {"stakeholder": 0.9, "regulatory": 0.9, "physical": 0.4, "augment": 1.2},
    "Product & Design":         {"stakeholder": 1.5, "regulatory": 0.7, "physical": 0.3, "augment": 1.0},
    "Quality & Testing":        {"stakeholder": 0.6, "regulatory": 0.7, "physical": 0.3, "augment": 1.3},
}
_DEFAULT_COEFFS = {"stakeholder": 1.0, "regulatory": 1.0, "physical": 0.5, "augment": 1.0}


# --- Seniority parsing ----------------------------------------------------
SENIORITY_ORDER = [
    "Junior", "Mid", "Senior", "Lead", "Staff", "Principal",
    "Director", "VP", "C-suite",
]
_SENIORITY_MULTIPLIER = {
    "Junior": 0.70, "Mid": 0.80, "Senior": 0.90, "Lead": 0.95,
    "Staff": 1.00, "Principal": 1.10, "Director": 1.20, "VP": 1.30, "C-suite": 1.40,
}

# Each pattern is matched in priority order against the role title. First match wins.
# The patterns are anchored to word boundaries — "Senior" must be a standalone word,
# not part of e.g. "Senior-Citizen Engineer".
_SENIORITY_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("C-suite",   re.compile(r"\b(Chief|CTO|CIO|CDO|CISO|CSO|CPO|CMO|CFO|CEO|COO)\b", re.IGNORECASE)),
    ("VP",        re.compile(r"\b(VP|Vice\s+President)\b", re.IGNORECASE)),
    ("Director",  re.compile(r"\b(Director|Head\s+of|Head)\b", re.IGNORECASE)),
    ("Principal", re.compile(r"\b(Principal|Distinguished|Fellow)\b", re.IGNORECASE)),
    ("Staff",     re.compile(r"\bStaff\b", re.IGNORECASE)),
    ("Senior",    re.compile(r"\b(Senior|Sr\.?)\b", re.IGNORECASE)),
    ("Lead",      re.compile(r"\bLead\b", re.IGNORECASE)),
    ("Junior",    re.compile(r"\b(Junior|Jr\.?|Associate|Intern|Graduate)\b", re.IGNORECASE)),
]


def parse_seniority(role_name: str) -> str:
    """Return one of SENIORITY_ORDER. Defaults to 'Mid' if no marker found."""
    for label, pat in _SENIORITY_PATTERNS:
        if pat.search(role_name):
            return label
    return "Mid"


# --- Role family (sub-category) ------------------------------------------
_FAMILY_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("AI & ML",         re.compile(r"\b(AI|ML|LLM|Machine\s+Learning|Deep\s+Learning|MLOps|Foundation\s+Model)\b", re.IGNORECASE)),
    ("Data",            re.compile(r"\b(Data\s+(Engineer|Scientist|Analyst)|Analytics|BI\b|Business\s+Intelligence|ETL)\b", re.IGNORECASE)),
    ("Security",        re.compile(r"\b(Security|SecOps|AppSec|GRC|Penetration|Forensic|SIEM|Compliance)\b", re.IGNORECASE)),
    ("Backend",         re.compile(r"\b(Backend|Server|API|Database|Distributed|Systems)\b", re.IGNORECASE)),
    ("Frontend",        re.compile(r"\b(Frontend|Front-end|UI\b|UX|React|Web\s+Developer)\b", re.IGNORECASE)),
    ("Mobile",          re.compile(r"\b(Mobile|iOS|Android|Flutter|React\s+Native)\b", re.IGNORECASE)),
    ("DevOps & SRE",    re.compile(r"\b(DevOps|SRE|Site\s+Reliability|Platform\s+Engineer|Infrastructure)\b", re.IGNORECASE)),
    ("Cloud",           re.compile(r"\b(Cloud|AWS|GCP|Azure|Kubernetes|Solutions\s+Architect)\b", re.IGNORECASE)),
    ("QA & Testing",    re.compile(r"\b(QA\b|Quality|Test\b|SDET|Automation\s+Engineer)\b", re.IGNORECASE)),
    ("Product",         re.compile(r"\b(Product\s+Manager|PM\b|Product\s+Owner|TPM)\b", re.IGNORECASE)),
    ("Design",          re.compile(r"\b(Designer|Design\s+|UX\s+Researcher)\b", re.IGNORECASE)),
    ("Hardware",        re.compile(r"\b(Hardware|Firmware|Embedded|FPGA|ASIC|Robotics|Electrical)\b", re.IGNORECASE)),
    ("Game",            re.compile(r"\b(Game\s+|Unreal|Unity|3D\s+|Graphics)\b", re.IGNORECASE)),
    ("Blockchain",      re.compile(r"\b(Blockchain|Crypto|Web3|Smart\s+Contract|Solidity)\b", re.IGNORECASE)),
]


def derive_role_family(role_name: str, category: str) -> str:
    """Return a sub-family label, falling back to the category if no pattern matches."""
    for label, pat in _FAMILY_PATTERNS:
        if pat.search(role_name):
            return label
    return category


# --- Physical-world dependency keywords ----------------------------------
_PHYSICAL_KEYWORDS = re.compile(
    r"\b(Hardware|Firmware|Embedded|Robotics|FPGA|ASIC|"
    r"On-?site|Field|Datacenter|Lab|Manufacturing|Drone|Sensor|Network\s+Engineer)\b",
    re.IGNORECASE,
)


# --- Derived score formulas ----------------------------------------------

def _clamp(v: float, lo: int = 0, hi: int = 10) -> int:
    return int(max(lo, min(hi, round(v))))


def human_judgment_score(automation_resistance: int, skill_depth: int) -> int:
    """Roles AI struggles with are typically high-AR and high-skill.

    Weighting: 60% automation resistance + 40% skill depth.
    """
    return _clamp(0.6 * automation_resistance + 0.4 * skill_depth)


def stakeholder_interaction_score(
    demand: int, strategic_importance: int, category: str, seniority: str
) -> int:
    """How much of the role is human coordination vs. solo execution.

    Stakeholder-heavy categories (Leadership, Product) lift the score.
    Seniority lifts it further — senior people manage relationships.
    """
    coeffs = CATEGORY_COEFFS.get(category, _DEFAULT_COEFFS)
    base = (demand + strategic_importance) / 2
    return _clamp(base * coeffs["stakeholder"] * _SENIORITY_MULTIPLIER[seniority] / 1.0)


def physical_world_dependency_score(role_name: str, category: str) -> int:
    """Most software roles score very low here; hardware/site/robotics roles lift it.

    Returns 0–10. Base from category coefficient, +3 if any physical keyword matches.
    """
    coeffs = CATEGORY_COEFFS.get(category, _DEFAULT_COEFFS)
    base = coeffs["physical"] * 5
    if _PHYSICAL_KEYWORDS.search(role_name):
        base += 3
    return _clamp(base)


def ai_augmentation_potential_score(automation_resistance: int, skill_depth: int) -> int:
    """Where AI can speed the role up without replacing it.

    High potential = low automation-resistance × high skill depth: the task is
    mechanically helpable, but a human still owns it. Capped 0–10.
    """
    inv_ar = 10 - automation_resistance
    return _clamp(0.5 * inv_ar + 0.5 * skill_depth)


def regulatory_relevance_score(strategic_importance: int, category: str) -> int:
    """Compliance / audit / regulated-industry exposure.

    Lifted heavily for Security and Leadership; otherwise category-default.
    """
    coeffs = CATEGORY_COEFFS.get(category, _DEFAULT_COEFFS)
    return _clamp(coeffs["regulatory"] * 5 + strategic_importance / 3.0)


# --- Confidence score ----------------------------------------------------

@dataclass
class ConfidenceInputs:
    has_live_postings: bool
    is_calibrated: bool   # one of the original 36 hand-scored roles
    has_salary_band: bool
    has_description: bool


def confidence_score(inputs: ConfidenceInputs) -> int:
    """0–100. Higher means more independent signals back the score for this role.

    Components:
      40  base (every role has the 4 base axes)
      +20 live posting count refreshed this week
      +20 originally hand-calibrated role (vs. extrapolated)
      +10 salary band populated
      +10 description populated
    """
    score = 40
    if inputs.has_live_postings:
        score += 20
    if inputs.is_calibrated:
        score += 20
    if inputs.has_salary_band:
        score += 10
    if inputs.has_description:
        score += 10
    return min(100, score)


# --- Narrative templates -------------------------------------------------
# Reasons rendered on the role detail page. Picked deterministically based
# on which sub-scores are highest / lowest. Templates are short and avoid
# overclaims — they restate the score, not make a guarantee.

_AXIS_LABEL = {
    "demand": "market demand",
    "automation_resistance": "automation resistance",
    "skill_depth": "skill depth",
    "strategic_importance": "strategic importance",
    "human_judgment": "human judgment",
    "stakeholder_interaction": "stakeholder interaction",
    "ai_augmentation_potential": "AI augmentation potential",
    "regulatory_relevance": "regulatory relevance",
}

_HIGH_RATIONALE = {
    "automation_resistance": "the methodology weights this most heavily for AI durability",
    "skill_depth": "depth of skill remains hard for current LLM tooling to substitute",
    "strategic_importance": "the role is positioned where companies under-staff at their peril",
    "human_judgment": "decisions still require human accountability and trade-off thinking",
    "stakeholder_interaction": "the work is largely human coordination, not artefact production",
    "regulatory_relevance": "the role sits inside a regulated workflow that humans must own",
    "demand": "hiring volume held up across the most recent labour-market data we ingest",
}

_LOW_CAVEAT = {
    "automation_resistance": "current code-assist tools cover a meaningful slice of the day-to-day output",
    "skill_depth": "much of the work is generalist and increasingly templated",
    "strategic_importance": "the role often slots into supporting rather than load-bearing functions",
    "demand": "posting volume softened year-over-year in our latest crawl",
    "ai_augmentation_potential": "the work isn't yet a strong fit for AI augmentation tooling",
}


def why_ai_resistant(scores: dict[str, int]) -> str:
    """Pick the two highest sub-scores (from a curated set) and template a reason."""
    candidates = {k: scores[k] for k in ("automation_resistance", "skill_depth", "strategic_importance", "human_judgment", "stakeholder_interaction") if k in scores}
    top = sorted(candidates.items(), key=lambda kv: -kv[1])[:2]
    if not top or top[0][1] < 6:
        return ""
    bits = []
    for axis, val in top:
        bits.append(f"{_AXIS_LABEL[axis]} ({val}/10) — {_HIGH_RATIONALE.get(axis, '')}")
    return "Highest on " + "; ".join(bits) + "."


def why_ai_exposed(scores: dict[str, int]) -> str:
    """Pick the two lowest sub-scores (from a curated set) and template a caveat."""
    candidates = {k: scores[k] for k in ("automation_resistance", "skill_depth", "strategic_importance", "demand") if k in scores}
    bot = sorted(candidates.items(), key=lambda kv: kv[1])[:2]
    if not bot or bot[0][1] > 6:
        return ""
    bits = []
    for axis, val in bot:
        bits.append(f"{_AXIS_LABEL[axis]} ({val}/10) — {_LOW_CAVEAT.get(axis, '')}")
    return "Watch points: " + "; ".join(bits) + "."
