"""OTA firmware version check endpoint.

Endpoint:
  - /control/otaUpgrade/getOtaVersion
"""

from __future__ import annotations

from typing import Any

from pybyd._api._common import ENDPOINT_NOT_SUPPORTED_CODES, build_inner_base, post_token_json
from pybyd._transport import Transport
from pybyd.config import BydConfig
from pybyd.session import Session

_ENDPOINT = "/control/otaUpgrade/getOtaVersion"
_NOT_SUPPORTED_CODES = ENDPOINT_NOT_SUPPORTED_CODES | frozenset({"1010"})


async def fetch_ota_version(
    config: BydConfig,
    session: Session,
    transport: Transport,
    vin: str,
) -> dict[str, Any]:
    """Fetch OTA firmware version info for a vehicle.

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
        not_supported_codes=_NOT_SUPPORTED_CODES,
    )
    return decoded if isinstance(decoded, dict) else {}
