"""Vehicle configuration endpoint.

Endpoint:
  - /vehicle/vehicleswitch/getLatestConfig
"""

from __future__ import annotations

from typing import Any

from pybyd._api._common import ENDPOINT_NOT_SUPPORTED_CODES, build_inner_base, post_token_json
from pybyd._transport import Transport
from pybyd.config import BydConfig
from pybyd.session import Session

_ENDPOINT = "/vehicle/vehicleswitch/getLatestConfig"


async def fetch_vehicle_config(
    config: BydConfig,
    session: Session,
    transport: Transport,
    vin: str,
) -> dict[str, Any]:
    """Fetch the latest vehicle configuration.

    Returns the raw decoded response dict since the structure varies
    across models and regions.
    """
    inner = build_inner_base(config, vin=vin)
    decoded = await post_token_json(
        endpoint=_ENDPOINT,
        config=config,
        session=session,
        transport=transport,
        inner=inner,
        vin=vin,
        not_supported_codes=ENDPOINT_NOT_SUPPORTED_CODES,
    )
    return decoded if isinstance(decoded, dict) else {}
