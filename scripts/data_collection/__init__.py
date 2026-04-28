"""Data collection pipelines.

Each module exposes a `collect()` callable that returns a structured payload
and writes a cached JSON/CSV file under data/raw/. Live network calls are
optional and clearly gated; cached data is the source of truth for the
analysis. Simulated datasets are clearly labeled with `data_kind: simulated`.
"""
