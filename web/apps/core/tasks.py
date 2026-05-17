"""Celery tasks for the core app."""
from __future__ import annotations

from celery import shared_task
from django.core.management import call_command


@shared_task(name="apps.core.tasks.refresh_postings")
def refresh_postings() -> str:
    """Run the live posting crawlers (HN, Greenhouse, Lever)."""
    call_command("refresh_postings")
    return "ok"
