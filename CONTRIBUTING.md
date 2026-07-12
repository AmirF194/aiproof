# Contributing to AIProof

Thanks for your interest in AIProof — a research project by [FastInfer Inc.](https://fastinfer.org)
that ranks 1,000+ technology roles by their expected resilience to AI automation over 2026–2035.

Contributions are welcome: bug fixes, data/source corrections, methodology improvements, and docs.
This guide covers how to get set up, the checks your change must pass, and the **hard rules** that
make this project defensible. Please read the hard rules before proposing anything that touches
scores, narrative text, or sources.

## Ground rules (read these first)

These are load-bearing constraints, not style preferences. A PR that breaks one will not be merged.

1. **No fabricated sources.** Every URL cited in the app must resolve and support the claim it backs.
   The source registry is [web/apps/core/sources.py](web/apps/core/sources.py).
2. **No hand-written or LLM-generated per-role prose.** Fields like `why_ai_resistant`,
   `why_ai_exposed`, key skills, and transition paths are either drawn from a real public dataset
   (O\*NET, BLS, etc.) or produced by a **deterministic formula** in
   [web/apps/roles/scoring.py](web/apps/roles/scoring.py). Never write per-role text by hand or with an
   LLM — change the formula or the input data instead.
3. **No overpromising.** Language stays restrained ("estimate", "directional analysis"). Never
   "guaranteed", "definitive", or "predicts".
4. **Public data only.** No paywalled, login-gated, or `robots.txt`-disallowed scraping. Only public
   APIs. Crawler ethics are published at [`/data-policy/`](https://aiproof.fastinfer.org/data-policy/).
5. **Preserve FastInfer branding** in the footer, nav, and structured-data Organization JSON-LD.

If your idea conflicts with one of these, open an issue to discuss before writing code — we may be
able to find an approach that fits.

## Getting set up

The app is Django + Celery on a five-container Docker Compose stack (API, worker, beat, Postgres,
Redis). You need Docker.

```bash
git clone https://github.com/FastInfer/aiproof.git
cd aiproof
cp .env.example .env          # fill in values; the defaults work for local dev
docker compose up -d --build
docker compose exec api python manage.py migrate
docker compose exec api python manage.py load_roles --wipe
```

Open <http://localhost:9012/>. Optionally pull live posting data with
`docker compose exec worker python manage.py refresh_postings`.

## The checks your change must pass

CI ([.github/workflows/deploy.yml](.github/workflows/deploy.yml)) gates every push and PR on lint +
tests. Run them locally before opening a PR:

```bash
docker compose exec -w /app api ruff check .          # lint (ruff, line-length 110)
docker compose exec -w /app api python -m pytest -q   # tests (pytest + pytest-django)
docker compose exec api python manage.py validate_data # data-integrity check
docker compose exec api python manage.py check         # Django system checks
```

A red CI run blocks merge. Fork PRs may show a failing **deploy** job — that step only runs on
pushes to `main` and needs secrets fork PRs can't access; it does not reflect your change.

## Changes that touch the data or scoring

Some files are single sources of truth — editing them ripples through the whole dataset:

- [web/apps/roles/scoring.py](web/apps/roles/scoring.py) — every derived-score formula, the seniority
  parser, the role-family classifier, and the narrative templates.
- [data/roles.csv](data/roles.csv) — the canonical role roster with the four base axes.
- [docs/role_directory.md](docs/role_directory.md) — one-line description per role.
- [web/apps/core/sources.py](web/apps/core/sources.py) — every data feed cited on `/sources/`.

If your change touches these, in the **same PR**:

- **Scoring formula change →** update the "Extended scoring" section of
  [METHODOLOGY.md](METHODOLOGY.md) so the math stays auditable, and run `validate_data`.
- **Roster / roles.csv change →** re-derive every role locally with
  `docker compose exec api python manage.py load_roles --wipe` and confirm `validate_data` passes.
- **New cited source →** add it to `sources.py` with a URL that resolves and supports the claim.

## Pull request expectations

- **One concern per PR**, branched off a fresh `main`. No unrelated refactors or reformatting.
- Match the surrounding code — naming, structure, and comment density.
- Include a test that would fail without your change where it makes sense.
- Write a clear PR description: what problem it solves, how you verified it, and any tradeoffs. If a
  reviewer needs to reproduce a bug, say how.
- Keep the app buildable at every commit — CI must be green.
- **Disclose AI assistance.** If you used an AI tool to help write the change, say so in the PR and
  confirm you understand and stand behind every line.

## Reporting bugs and proposing changes

Open an issue using one of the templates:

- **Bug report** — something in the app is broken or wrong.
- **Data / source correction** — a score, description, or cited source looks off. Include the role and
  the public evidence.
- **Feature / methodology proposal** — a new dimension, feed, or scoring idea. Check it against the
  ground rules above first.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE) that
covers this project.
