"""Feature toggle data models."""

from __future__ import annotations

from pybyd.models._base import BydBaseModel


class FeatureToggle(BydBaseModel):
    """A single vehicle feature toggle."""

    function_code: str = ""
    """Unique identifier for the feature (e.g. ``sentry``, ``autoLock``)."""
    function_name: str = ""
    """Human-readable feature name."""
    enabled: bool = False
    """Whether the feature is currently enabled."""


class FeatureToggles(BydBaseModel):
    """Collection of all vehicle feature toggles."""

    toggles: list[FeatureToggle] = []
    """List of individual feature toggles."""

    def get(self, function_code: str) -> FeatureToggle | None:
        """Look up a toggle by function code."""
        for toggle in self.toggles:
            if toggle.function_code == function_code:
                return toggle
        return None

    @property
    def enabled_codes(self) -> set[str]:
        """Return set of function codes that are enabled."""
        return {t.function_code for t in self.toggles if t.enabled}
