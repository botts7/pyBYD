"""Sentry mode data models."""

from __future__ import annotations

from pybyd.models._base import BydBaseModel, BydEnum


class SentryStatus(BydEnum):
    """Sentry mode status values from realtime data ``sentryStatus``."""

    OFF = 0
    ON = 1
    TRIGGERED = 2


class SentryModeResult(BydBaseModel):
    """Result of a sentry mode toggle command."""

    success: bool = False
    """Whether the command completed successfully."""
    sentry_enabled: bool = False
    """Target sentry state that was requested."""
