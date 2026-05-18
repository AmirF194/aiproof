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
    ("Frontend",        re.compile(r"\b(Frontend|Front-end|UI\s+Engineer|React|Web\s+Developer)\b", re.IGNORECASE)),
    ("Mobile",          re.compile(r"\b(Mobile|iOS|Android|Flutter|React\s+Native)\b", re.IGNORECASE)),
    ("DevOps & SRE",    re.compile(r"\b(DevOps|SRE|Site\s+Reliability|Platform\s+Engineer|Infrastructure)\b", re.IGNORECASE)),
    ("Cloud",           re.compile(r"\b(Cloud|AWS|GCP|Azure|Kubernetes|Solutions\s+Architect)\b", re.IGNORECASE)),
    ("QA & Testing",    re.compile(r"\b(QA\b|Quality|Test\b|SDET|Automation\s+Engineer)\b", re.IGNORECASE)),
    ("Product",         re.compile(r"\b(Product\s+Manager|PM\b|Product\s+Owner|TPM)\b", re.IGNORECASE)),
    ("Design",          re.compile(r"\b(Designer|UX\s+Researcher|Design\s+Lead|Design\s+Director|UI\s+Designer)\b", re.IGNORECASE)),
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


# --- Role enrichment templates (Phase 10) --------------------------------
# Deterministic per-family content rendered on the role detail page so every
# role has an "overview / responsibilities / tools / day-to-day / AI impact"
# section instead of just a one-line note. Same rule as why_ai_resistant:
# the prose is a fixed template selected by attributes (role_family + category
# + seniority), never generated per role. Two roles with the same (family,
# category, seniority) tuple render identical enrichment. The detail page
# discloses this so users don't mistake it for researched-per-role prose.

_OVERVIEW: dict[str, str] = {
    # --- Families (preferred when set) ---
    "Backend": "Backend engineers build the server-side systems, APIs, and data pipelines that power applications. The work centres on data modelling, service design, debugging distributed-system failures, and keeping production infrastructure reliable under real-world load.",
    "Frontend": "Frontend engineers build the browser-facing layer of web applications — the markup, styling, interactivity, and state management end users actually touch. Performance, accessibility, and design-system fidelity are the day-to-day quality bars.",
    "Mobile": "Mobile engineers ship the iOS or Android apps users carry on their devices. The work spans platform-native UI, offline-first data sync, integration with device sensors, and the long-tail of release-engineering through app-store review.",
    "AI & ML": "AI and ML roles cover the full pipeline from data preparation through model training to serving inference at production scale. Most of the work is data cleaning, evaluation infrastructure, and integration plumbing — model architecture choices are a smaller slice than headlines suggest.",
    "Data": "Data roles span the spectrum from pipeline construction (data engineering) through analysis and modelling (data science) to dashboard delivery (analytics). The common thread is turning raw event streams into trusted, queryable datasets that downstream teams can rely on.",
    "Security": "Security engineers harden systems against attack — auditing code, designing identity and access controls, running detection and response, and partnering with compliance on regulated workflows. The work is part research, part engineering, part incident response.",
    "DevOps & SRE": "DevOps and Site Reliability engineers own how software gets built, deployed, and kept running. They build the CI/CD plumbing, the observability stack, the on-call rotation, and the platform abstractions that let product teams ship without inventing infrastructure from scratch.",
    "Cloud": "Cloud engineers design and operate the AWS/GCP/Azure footprint an organisation runs on — networking, IAM, account topology, cost controls, and the reference architectures product teams adopt.",
    "QA & Testing": "Quality engineers build the test infrastructure that catches regressions before customers do — unit and integration suites, end-to-end automation, performance baselines, and the release-gate processes that decide what ships.",
    "Product": "Product managers own what gets built and why. The work is talking to users, framing problems, prioritising trade-offs, writing the spec that engineering can build against, and shepherding launches across design, engineering, marketing, and support.",
    "Design": "Designers — product, UX, visual, research — shape how users experience the software. The work spans research interviews, flow design, prototyping, design-system contribution, and tight collaboration with engineering on what's actually buildable.",
    "Hardware": "Hardware and firmware engineers design physical computing devices and the embedded software that runs on them. The work is inherently slower than pure software — silicon and PCBs have lead times measured in weeks or months, not minutes.",
    "Game": "Game developers build interactive entertainment software — engine work, gameplay programming, graphics, tools, and live-service operations. The discipline blends real-time systems engineering with creative collaboration alongside artists and designers.",
    "Blockchain": "Blockchain engineers build on-chain protocols, smart contracts, and the off-chain infrastructure (indexers, RPC nodes, wallets) that makes them usable. Security review and economic design are first-class concerns, not afterthoughts.",
    # --- Categories (fallback when no family matched) ---
    "Engineering": "Software engineers turn product requirements into working systems — designing, writing, testing, deploying, and operating code that runs in production. The mix of greenfield design vs. maintenance, and of solo work vs. coordination, varies wildly by company stage and seniority.",
    "Engineering Leadership": "Engineering leadership roles own how a technical organisation operates: architecture direction, team structure, hiring, budget, and the trade-off conversations between speed, quality, and cost. The IC track (Staff / Principal / Distinguished) and the management track (EM / Director / VP) diverge here.",
    "Data & AI": "Data and AI roles cover the full life-cycle of turning raw signals into product features — instrumentation, pipelines, modelling, evaluation, and serving. AI/ML specialisations sit on top of a much larger surface area of plumbing that has to work first.",
    "Platform & Infrastructure": "Platform and infrastructure roles build the substrate other engineers depend on — the deploy pipeline, the observability stack, the internal developer platform, the cloud account topology. The customer is other engineers; the bar is invisibility (when it works) and immediate diagnosis (when it doesn't).",
    "Product & Design": "Product and design roles define what gets built and shape how users experience it. The work bridges customer research, business strategy, visual craft, and the cross-functional negotiation that turns ideas into shipped features.",
    "Quality & Testing": "Quality and testing roles build the safety net that catches issues before customers do — test infrastructure, automation, performance and security baselines, and the release-gate processes that decide what ships when.",
    "Specialized & Emerging": "Specialised and emerging roles sit at the frontier of computing — hardware, robotics, embedded systems, blockchain, games, and other domains where the engineering loop is shaped by physics, regulation, or novel computing models rather than typical web/cloud constraints.",
}

_RESPONSIBILITIES: dict[str, list[str]] = {
    "Backend": [
        "Design REST/gRPC APIs and the data models behind them",
        "Build and maintain services that handle production traffic",
        "Debug distributed-system failures across logs, traces, and metrics",
        "Review code from peers and mentor more junior engineers",
        "Participate in on-call rotation for the services the team owns",
        "Write integration tests and run performance baselines before release",
        "Document architecture decisions and trade-offs for future readers",
    ],
    "Frontend": [
        "Implement UI components from designs while preserving design-system invariants",
        "Manage client-side state and data-fetching for complex flows",
        "Optimise bundle size, render performance, and Core Web Vitals",
        "Ensure accessibility (keyboard nav, screen-reader semantics, contrast)",
        "Cross-browser test and triage device-specific regressions",
        "Collaborate with designers on prototypes and feasibility reviews",
        "Maintain Storybook or equivalent component documentation",
    ],
    "Mobile": [
        "Build platform-native UI screens and navigation flows",
        "Handle offline-first data sync, background tasks, and push notifications",
        "Integrate with device sensors, camera, location, and OS permissions",
        "Manage app-store releases, phased rollouts, and crash-rate monitoring",
        "Profile performance on low-end devices and tight battery budgets",
        "Coordinate with backend engineers on mobile-friendly API contracts",
    ],
    "AI & ML": [
        "Build training and evaluation pipelines for production models",
        "Clean, label, and curate training data — usually the bulk of the work",
        "Run experiments and document why one approach beat another",
        "Deploy models to inference infrastructure with monitoring and rollback",
        "Investigate offline/online metric divergence and model drift",
        "Partner with product teams to scope what an ML solution can/can't do",
    ],
    "Data": [
        "Build ingestion pipelines from source systems into the warehouse",
        "Model data into dimensional or denormalised tables downstream teams use",
        "Implement data-quality checks and SLAs for critical tables",
        "Write SQL and dashboards that answer business questions",
        "Document table lineage, freshness, and semantic meaning",
        "Investigate metric anomalies before they reach exec dashboards",
    ],
    "Security": [
        "Threat-model new systems and write secure-design reviews",
        "Audit code and infrastructure for known vulnerability classes",
        "Run incident response when alerts fire — investigate, contain, post-mortem",
        "Build detection content (SIEM rules, EDR queries, anomaly baselines)",
        "Partner with compliance on audit evidence for SOC 2 / ISO / PCI / HIPAA",
        "Educate other engineering teams on security trade-offs in their designs",
    ],
    "DevOps & SRE": [
        "Own the CI/CD pipeline end-to-end and the deploy story",
        "Run the observability stack — logs, metrics, traces, alerting",
        "Lead incident response and write blameless post-mortems",
        "Build platform tooling that abstracts infra away from product teams",
        "Manage cloud-cost budgets and right-size compute over time",
        "Improve reliability against measured SLOs, not vibes",
    ],
    "Cloud": [
        "Design cloud account topology, networking, and IAM boundaries",
        "Build reference architectures product teams adopt and extend",
        "Manage cost allocation, reserved-capacity planning, and FinOps reviews",
        "Implement infrastructure-as-code modules for repeatable deployments",
        "Partner with security on cloud-posture and compliance controls",
    ],
    "QA & Testing": [
        "Build and maintain end-to-end test suites for critical user flows",
        "Triage failing tests — bug vs. flake — and drive resolution",
        "Set up performance and load testing baselines for release gates",
        "Partner with developers on testability and test-pyramid hygiene",
        "Run exploratory testing for features that automation can't reach",
        "Maintain release-readiness reports for product and engineering leadership",
    ],
    "Product": [
        "Talk to customers and synthesise insights into product opportunities",
        "Write specs, PRDs, or one-pagers that align engineering and design",
        "Prioritise the backlog against business goals and technical capacity",
        "Define and track success metrics for shipped features",
        "Coordinate launches across engineering, marketing, support, and sales",
        "Sunset features that aren't earning their maintenance cost",
    ],
    "Design": [
        "Run user research — interviews, usability tests, diary studies",
        "Produce wireframes, prototypes, and high-fidelity mocks",
        "Contribute to and maintain the design system",
        "Pair with engineering on feasibility and interaction details",
        "Review shipped work against the spec and file polish bugs",
        "Tell the visual story for launches, demos, and exec reviews",
    ],
    "Hardware": [
        "Design schematics, PCBs, or HDL for new hardware revisions",
        "Bring up new boards and characterise them against spec",
        "Write firmware and drivers, often in C/C++ or Rust on bare metal",
        "Run thermal, EMC, and reliability testing in the lab",
        "Coordinate with manufacturing on DFM and yield improvements",
        "Debug field failures back to root cause through silicon, firmware, or assembly",
    ],
    "Game": [
        "Implement gameplay systems and engine features in C++ or game-engine scripting",
        "Build tools content creators use daily",
        "Profile rendering and CPU/GPU performance to hit frame-rate targets",
        "Integrate with platform SDKs (consoles, mobile stores, Steam)",
        "Support live-service operations, hotfixes, and patch cadences",
    ],
    "Blockchain": [
        "Write and audit Solidity, Rust, or Move smart contracts",
        "Build off-chain infrastructure (indexers, RPC providers, oracle integrations)",
        "Model token mechanics and economic incentives with security in mind",
        "Run protocol upgrade processes and governance integrations",
        "Partner with auditors before any mainnet deployment",
    ],
    "Engineering": [
        "Design and build features end-to-end based on product requirements",
        "Review code, mentor more junior engineers, and unblock teammates",
        "Debug production issues, often across multiple services",
        "Write tests and documentation for the work you ship",
        "Participate in technical-design discussions and architecture reviews",
        "Carry pager duty for the systems your team owns",
    ],
    "Engineering Leadership": [
        "Set technical direction and architecture priorities across teams",
        "Hire, grow, and (when needed) performance-manage engineers",
        "Own budget, headcount, and roadmap negotiations with peers",
        "Translate exec strategy into team-level execution plans",
        "Run the engineering operating cadence — planning, retros, reviews",
        "Communicate state-of-engineering to the rest of the company",
    ],
    "Data & AI": [
        "Instrument data collection from product surfaces and source systems",
        "Build pipelines and warehouse models downstream teams query against",
        "Develop and evaluate ML models against well-defined offline metrics",
        "Ship inference services and monitor for drift in production",
        "Communicate uncertainty honestly — confidence intervals, not point estimates",
    ],
    "Platform & Infrastructure": [
        "Build internal platforms product teams adopt to ship faster",
        "Own the deploy pipeline, observability, and on-call infrastructure",
        "Manage cloud capacity, cost, and security posture",
        "Lead incident response and write blameless post-mortems",
        "Define platform SLOs and report against them honestly",
    ],
    "Product & Design": [
        "Define what to build and why through research and prioritisation",
        "Translate strategy into specs, prototypes, and roadmaps",
        "Partner with engineering on trade-offs and feasibility",
        "Coordinate launches and the cross-functional work around them",
        "Track success metrics and feed them back into prioritisation",
    ],
    "Quality & Testing": [
        "Build automated test coverage for critical user journeys",
        "Triage failures and drive root-cause analysis",
        "Set and report against release-readiness criteria",
        "Improve test infrastructure speed, reliability, and signal",
        "Champion testability practices upstream into engineering",
    ],
    "Specialized & Emerging": [
        "Apply engineering discipline to domains with non-software constraints",
        "Build prototypes that prove out novel approaches",
        "Coordinate with specialists outside software (EE, mechanical, legal, etc.)",
        "Document hard-won knowledge in fast-moving fields",
        "Bridge between research and production engineering",
    ],
}

_TOOLS: dict[str, list[str]] = {
    "Backend": ["Python or Go", "Java/Kotlin or C#", "PostgreSQL", "Redis", "Kafka or RabbitMQ", "Docker", "Kubernetes", "AWS/GCP/Azure", "OpenTelemetry", "Git + CI"],
    "Frontend": ["TypeScript", "React or Vue", "Next.js / Remix", "Tailwind or CSS-in-JS", "Webpack/Vite", "Storybook", "Playwright/Cypress", "Lighthouse"],
    "Mobile": ["Swift / SwiftUI", "Kotlin / Jetpack Compose", "React Native or Flutter", "Xcode + Android Studio", "Firebase", "Fastlane", "App Store Connect / Google Play Console"],
    "AI & ML": ["Python", "PyTorch or JAX", "Hugging Face Transformers", "scikit-learn", "Ray or Kubeflow", "Weights & Biases / MLflow", "BigQuery / Snowflake", "vLLM or Triton"],
    "Data": ["SQL (BigQuery / Snowflake / Postgres)", "dbt", "Airflow or Dagster", "Python (pandas / Polars)", "Spark", "Looker / Tableau / Metabase", "Fivetran / Airbyte", "Great Expectations"],
    "Security": ["Burp Suite", "Nessus / Qualys", "Splunk / Elastic SIEM", "CrowdStrike or SentinelOne", "Vault", "Terraform (for IAM)", "AWS GuardDuty / Azure Defender", "OWASP ZAP", "YARA / Sigma"],
    "DevOps & SRE": ["Terraform", "Kubernetes", "Helm / Kustomize", "ArgoCD or Flux", "Prometheus + Grafana", "Datadog or New Relic", "GitHub Actions / GitLab CI", "PagerDuty", "Ansible"],
    "Cloud": ["AWS, GCP, or Azure", "Terraform / Pulumi", "Kubernetes (EKS/GKE/AKS)", "CloudFormation", "AWS CDK", "FinOps tooling (CUR / Vantage / CloudHealth)", "Service-mesh (Istio / Linkerd)"],
    "QA & Testing": ["Playwright / Cypress / Selenium", "JUnit / pytest / Jest", "k6 / JMeter / Locust", "Allure / TestRail", "BrowserStack / Sauce Labs", "Postman", "GitHub Actions / Jenkins"],
    "Product": ["Linear / Jira", "Figma", "Amplitude / Mixpanel / Heap", "Looker / Mode", "Notion / Confluence", "Productboard / Aha", "Pendo / Intercom"],
    "Design": ["Figma", "FigJam / Miro", "Adobe Creative Suite", "Principle / ProtoPie", "Maze / UserTesting", "Storybook (for design-system handoff)", "Lottie"],
    "Hardware": ["KiCad / Altium", "Oscilloscope + logic analyser", "C/C++ / Rust", "FreeRTOS / Zephyr", "Verilog / VHDL", "JTAG debuggers", "MATLAB / Simulink"],
    "Game": ["Unreal Engine / Unity", "C++ / C#", "Perforce / Plastic SCM", "Maya / Blender (for tooling)", "RenderDoc / PIX", "Wwise / FMOD", "Platform SDKs (PlayStation, Xbox, Switch)"],
    "Blockchain": ["Solidity / Vyper", "Hardhat or Foundry", "Rust (Anchor for Solana)", "Move (Aptos/Sui)", "ethers.js / web3.js", "Tenderly", "Slither / Mythril", "The Graph"],
    "Engineering": ["Python / Go / TypeScript / Java", "Git", "Docker", "Kubernetes", "PostgreSQL", "AWS / GCP / Azure", "GitHub / GitLab", "Jira / Linear"],
    "Engineering Leadership": ["Linear / Jira", "Notion / Confluence", "Lattice / 15Five", "Greenhouse / Ashby (ATS)", "Looker / Mode (for engineering metrics)", "PagerDuty"],
    "Data & AI": ["Python", "SQL", "PyTorch / scikit-learn", "Spark", "Airflow / Dagster", "dbt", "Snowflake / BigQuery", "MLflow / Weights & Biases"],
    "Platform & Infrastructure": ["Terraform", "Kubernetes", "Prometheus + Grafana", "Datadog", "ArgoCD", "GitHub Actions", "PagerDuty", "AWS / GCP / Azure"],
    "Product & Design": ["Figma", "Linear / Jira", "Amplitude / Mixpanel", "Notion / Confluence", "Loom", "Maze / UserTesting", "Looker / Mode"],
    "Quality & Testing": ["Playwright / Cypress", "pytest / Jest", "k6 / JMeter", "Allure / TestRail", "GitHub Actions / Jenkins", "BrowserStack"],
    "Specialized & Emerging": ["Domain-specific stacks (varies)", "C / C++ / Rust", "MATLAB / Simulink (where applicable)", "Hardware lab equipment", "Industry simulation tools"],
}

_DAY_TO_DAY: dict[str, str] = {
    "Backend": "A typical day mixes design discussion (1–2 hours of meetings or async review), focused coding on the current sprint feature (3–4 hours), and a long tail of code review, on-call triage, and unblocking teammates. Production incidents reshuffle the day when they happen.",
    "Frontend": "Mornings tend to be focused build time on the current component or flow; afternoons drift into design review, accessibility QA, and pairing with backend on API contracts. Browser-specific bug investigation is the unpredictable interrupter.",
    "Mobile": "Build cycles are slower than web — emulator and device-farm time dominates the inner loop. The week is shaped around the app-store release cadence, with crash-rate triage and phased-rollout monitoring after each ship.",
    "AI & ML": "Most of the day is data inspection, evaluation analysis, and infrastructure plumbing — far less model-architecture work than the discipline's reputation suggests. Long training runs reshape the schedule around them.",
    "Data": "Morning standups touch the day's dashboard requests and pipeline alerts. The bulk of the day is SQL, dbt model work, and chasing data-quality anomalies — punctuated by ad-hoc analyst requests from stakeholders.",
    "Security": "Days oscillate between deep-focus work (threat modelling, code audits, detection-engineering) and reactive work (alert triage, incident response, compliance evidence requests). On-call weeks are heavily reactive; non-on-call weeks resemble a normal engineering schedule.",
    "DevOps & SRE": "Operational work dominates when systems are unhappy — alerts, capacity issues, deploy failures. When systems are happy, days shift to platform work, automation improvements, and post-mortem follow-ups.",
    "Cloud": "Long focused stretches of architecture design or Terraform module work, interrupted by cost reviews, IAM access requests from other teams, and the occasional production-incident escalation that needs an architecture-level view.",
    "QA & Testing": "Days follow the release calendar — early in the cycle is automation work and test-coverage expansion; late in the cycle is regression triage, exploratory testing, and release-readiness reviews.",
    "Product": "Days are heavily meeting-driven — customer calls, design reviews, engineering syncs, exec updates. Focus work (writing specs, analysing data, prioritising the backlog) happens between meetings or at the edges of the day.",
    "Design": "Mornings are typically focused craft work in Figma; afternoons are reviews, research sessions, and pairing with engineering. The week is shaped by sprint cadences and design-critique sessions.",
    "Hardware": "Days are paced by board lead times and lab equipment availability — a schematic review in the morning might be followed by an afternoon characterising a board on a logic analyser. Iterations are days-to-weeks, not minutes.",
    "Game": "Days blend systems engineering with creative collaboration — gameplay code in the morning, a playtest in the afternoon, a tools-feature request from the art team in between. Crunch periods are real but increasingly contested in modern studios.",
    "Blockchain": "Days mix protocol-level engineering with audit-mindset review of teammates' code. Mainnet deployment days are tense set-pieces; surrounding days are upgrade planning, governance proposals, and integration work.",
    "Engineering": "A typical day mixes 2–3 hours of focused build time on the current feature, 1–2 hours of code review and async collaboration, and meetings (standup, design reviews, 1:1s) filling the remainder. On-call weeks shift the balance toward investigation and recovery.",
    "Engineering Leadership": "Days are mostly meetings — 1:1s with reports, peer-leader syncs, planning sessions, exec updates. Focus work (writing strategy docs, reviewing architecture proposals) happens early morning, late evening, or in deliberately blocked stretches.",
    "Data & AI": "Days alternate between data inspection, experiment design, modelling work, and stakeholder syncs explaining results in business terms. Long training runs and pipeline runs anchor the schedule around them.",
    "Platform & Infrastructure": "Operational work dominates when production is unhappy; platform-improvement work fills the calmer days. The week is shaped by on-call rotations, capacity planning cycles, and the cost-review cadence.",
    "Product & Design": "Days are heavily collaborative — customer interviews, design reviews, engineering syncs, exec updates — interleaved with focused craft (specs, prototypes, analysis).",
    "Quality & Testing": "Days follow the release calendar — automation expansion early in the cycle, regression triage and release-readiness work late in the cycle. Flaky-test investigation is the unpredictable interrupter.",
    "Specialized & Emerging": "Days are shaped by the domain's pace — hardware lead times, regulatory review cycles, audit windows, or live-service patch schedules — rather than a pure software cadence.",
}

_AI_IMPACT: dict[str, str] = {
    "Backend": "Code-assist tools (Copilot, Cursor, Claude Code) have eaten the boilerplate end of the work — CRUD endpoints, getters/setters, glue code, ORM scaffolding. Architectural choices, debugging distributed-system failures, capacity planning, and on-call judgement remain stubbornly human-owned.",
    "Frontend": "AI assistance is strong for component scaffolding, Tailwind classes, and translating designs to JSX. It's still weak at design-system fidelity, cross-browser nuance, accessibility audits, and the taste-driven decisions about when a UI 'feels right'.",
    "Mobile": "Code completion works well for boilerplate (view layout, lifecycle methods). The platform-specific knowledge — App Store / Play Store review, OS update fallout, device-specific bugs — is where current AI tooling is least useful.",
    "AI & ML": "Ironically, ML roles are not the most AI-augmented — the work is heavily about evaluating models, curating data, and reasoning about training dynamics, which current LLM tools don't help with much. The boilerplate (training loops, data loaders) is the part that benefits.",
    "Data": "SQL generation and dbt model scaffolding are increasingly LLM-assisted. The semantic layer — knowing what a metric actually means in business terms, and what makes a number wrong — is the durable human skill.",
    "Security": "AI helps with detection-rule writing, code-review triage, and report drafting. The adversarial thinking, incident response under pressure, and compliance judgement remain entirely human — and being right matters more than being fast.",
    "DevOps & SRE": "AI assists with Terraform modules, runbook drafting, and post-mortem narrative. Incident response itself — the situational awareness during a P0 — is too high-stakes to delegate. So is the multi-year platform strategy.",
    "Cloud": "Architecture diagram-to-Terraform translation is a real productivity win. Cost optimisation, IAM design, and multi-account governance still require human judgement about organisational structure and risk tolerance.",
    "QA & Testing": "Test generation is a clear AI win for unit and integration tests. End-to-end test stability, exploratory testing, and the judgement of 'is this safe to ship' remain human responsibilities.",
    "Product": "Spec drafting, research synthesis, and competitor analysis are AI-assistable today. The hard parts — choosing what to build, saying no, navigating cross-functional politics, and being accountable for outcomes — don't outsource cleanly.",
    "Design": "AI is strong at variation generation, layout suggestions, and copy. It's weak at the strategic 'what should this product even feel like' question and at the trust-building that comes from a designer the team has worked with for years.",
    "Hardware": "AI helps with HDL drafting, datasheet summarisation, and firmware boilerplate. The physical-world steps (lab characterisation, manufacturing partnership, regulatory certification) bound how fast hardware can move regardless of software-side AI gains.",
    "Game": "AI accelerates asset variation, dialogue drafting, and tooling code. The creative direction, level design, and the live-service relationship with players are where the durable human work sits.",
    "Blockchain": "AI helps with Solidity scaffolding and integration code. Audit-grade review and economic-mechanism design are too consequential (and too adversarial) to delegate.",
    "Engineering": "Code-assist tools have changed the day-to-day for nearly every engineer — boilerplate, syntax recall, and unfamiliar-API exploration are much faster. Architectural judgement, debugging novel failures, and the cross-functional negotiation of what to build remain firmly human.",
    "Engineering Leadership": "AI assists with status drafting, doc summarisation, and analytical work. The substance of leadership — hiring, performance, technical direction, organisational politics — is precisely the kind of accountability that can't be delegated to a tool.",
    "Data & AI": "Data and ML roles benefit at the plumbing layer (SQL, training-loop scaffolding) and at result communication (chart drafting, exec-deck writing). The judgement of which model to trust, which metric to optimise, and what the numbers actually mean remains human.",
    "Platform & Infrastructure": "Infrastructure-as-code drafting, runbook generation, and incident-summary writing are AI-assisted today. Live incident response and multi-year platform direction stay human-owned.",
    "Product & Design": "AI accelerates the artefact production (specs, mocks, copy) but not the judgement (what to build, what's worth saying no to). The customer empathy and cross-functional accountability are the durable parts.",
    "Quality & Testing": "Test generation is a near-term productivity win. Exploratory testing and the 'should this ship' judgement remain human.",
    "Specialized & Emerging": "AI impact varies by domain — strong where there's a software-engineering inner loop (game tooling, smart contracts), weaker where physics or regulation set the cadence (hardware, robotics in regulated industries).",
}

_SENIORITY_SCOPE: dict[str, str] = {
    "Junior": "Junior roles are well-scoped under direct supervision; deliberate skill-building is part of the deliverable, not a side-effect.",
    "Mid": "Mid-level engineers own medium-scope features end-to-end, with code review as the main calibration loop and a growing expectation of architectural opinion.",
    "Senior": "Senior engineers drive design within their area, mentor more junior engineers, and are expected to push back on bad requirements rather than just execute them.",
    "Lead": "Lead engineers run technical delivery for a small team — still writing code daily, but increasingly responsible for the roadmap and the team's technical decisions.",
    "Staff": "Staff engineers set direction across multiple teams; the highest-leverage IC track at most companies. Code contribution drops; design influence and cross-team unblocking rise.",
    "Principal": "Principal engineers are company-wide technical authorities — multi-year platform direction, hardest cross-team problems, and senior-IC mentorship across the org.",
    "Director": "Directors manage managers (or a large single team). The day-to-day shifts from individual contribution to organisational health, hiring, and exec-level alignment.",
    "VP": "VPs own an entire function (Engineering, Product, Design) — budget, headcount, exec strategy. Most work is org-level rather than craft-level.",
    "C-suite": "C-suite leaders have executive accountability for a discipline at company scale. Outcomes are measured in business terms; reports run to the CEO or board.",
}


def _enrichment_key(role_family: str, category: str, dictionary: dict[str, str | list[str]]) -> str:
    """Pick the family if we have content for it, otherwise the category, otherwise 'Engineering'."""
    if role_family in dictionary:
        return role_family
    if category in dictionary:
        return category
    return "Engineering"


def role_overview(role_family: str, category: str, seniority: str) -> str:
    key = _enrichment_key(role_family, category, _OVERVIEW)
    base = _OVERVIEW[key]
    scope = _SENIORITY_SCOPE.get(seniority, "")
    return f"{base} {scope}".strip()


def role_responsibilities(role_family: str, category: str) -> list[str]:
    key = _enrichment_key(role_family, category, _RESPONSIBILITIES)
    return list(_RESPONSIBILITIES[key])


def role_typical_tools(role_family: str, category: str) -> list[str]:
    key = _enrichment_key(role_family, category, _TOOLS)
    return list(_TOOLS[key])


def role_day_to_day(role_family: str, category: str) -> str:
    key = _enrichment_key(role_family, category, _DAY_TO_DAY)
    return _DAY_TO_DAY[key]


def role_ai_impact(role_family: str, category: str) -> str:
    key = _enrichment_key(role_family, category, _AI_IMPACT)
    return _AI_IMPACT[key]
