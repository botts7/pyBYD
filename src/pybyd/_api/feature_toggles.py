"""Vehicle feature toggle endpoints.

Endpoints:
  - /vehicle/vehicleswitch/getVinSwitchState (get all toggles)
  - /vehicle/vehicleswitch/setVinSwitchState (set a toggle)

Feature toggles control per-vehicle settings like sentry mode,
auto-lock, speed alerts, and other configurable features.
"""

from __future__ import annotations

import logging
from typing import Any

from pybyd._api._common import ENDPOINT_NOT_SUPPORTED_CODES, build_inner_base, post_token_json
from pybyd._transport import Transport
from pybyd.config import BydConfig
from pybyd.models.feature_toggle import FeatureToggle, FeatureToggles
from pybyd.session import Session

_logger = logging.getLogger(__name__)

_GET_ENDPOINT = "/vehicle/vehicleswitch/getVinSwitchState"
_SET_ENDPOINT = "/vehicle/vehicleswitch/setVinSwitchState"


async def fetch_feature_toggles(
    config: BydConfig,
    session: Session,
    transport: Transport,
    vin: str,
) -> FeatureToggles:
    """Fetch all feature toggles for a vehicle."""
    inner = build_inner_base(config, vin=vin)
    decoded = await post_token_json(
        endpoint=_GET_ENDPOINT,
        config=config,
        session=session,
        transport=transport,
        inner=inner,
        vin=vin,
        not_supported_codes=ENDPOINT_NOT_SUPPORTED_CODES,
    )
    return _parse_toggles(decoded)


async def set_feature_toggle(
    config: BydConfig,
    session: Session,
    transport: Transport,
    vin: str,
    function_code: str,
    *,
    enable: bool,
) -> Any:
    """Set a single feature toggle on/off.

    .. warning::
        This endpoint is untested on a real vehicle. The available
        ``function_code`` values are model-dependent and not fully
        documented. Use ``fetch_feature_toggles`` first to discover
        valid codes for a given vehicle.
    """
    inner = build_inner_base(config, vin=vin)
    inner["functionCode"] = function_code
    inner["state"] = "1" if enable else "0"
    return await post_token_json(
        endpoint=_SET_ENDPOINT,
        config=config,
        session=session,
        transport=transport,
        inner=inner,
        vin=vin,
        not_supported_codes=ENDPOINT_NOT_SUPPORTED_CODES,
    )


def _parse_toggles(data: Any) -> FeatureToggles:
    """Parse raw toggle response into model."""
    toggles: list[FeatureToggle] = []
    if isinstance(data, dict):
        items = data.get("list") or data.get("switchList") or []
        if isinstance(items, list):
            for item in items:
                if not isinstance(item, dict):
                    continue
                toggles.append(
                    FeatureToggle(
                        function_code=str(item.get("functionCode", "")),
                        function_name=str(item.get("functionName", "")),
                        enabled=item.get("state") in (1, "1", True),
                    )
                )
    return FeatureToggles(toggles=toggles)
