"""Full climate/HVAC status endpoint (getRefrigeratorNow).

Despite the name, ``/control/getRefrigeratorNow`` returns the complete
HVAC state including A/C, seat heating/ventilation, steering wheel heat,
defrost, air quality, and refrigerator status.  It provides more fields
than the standard ``/control/getStatusNow`` endpoint.

Endpoint:
  - /control/getRefrigeratorNow
"""

from __future__ import annotations

from pybyd._api._common import ENDPOINT_NOT_SUPPORTED_CODES, build_inner_base, post_token_json
from pybyd._transport import Transport
from pybyd.config import BydConfig
from pybyd.models.hvac import HvacStatus
from pybyd.session import Session

_ENDPOINT = "/control/getRefrigeratorNow"
_NOT_SUPPORTED_CODES = ENDPOINT_NOT_SUPPORTED_CODES | frozenset({"1009"})


async def fetch_full_climate_status(
    config: BydConfig,
    session: Session,
    transport: Transport,
    vin: str,
) -> HvacStatus:
    """Fetch full climate/HVAC status via ``/control/getRefrigeratorNow``.

    Returns the same ``HvacStatus`` model as ``fetch_hvac_status`` but
    with additional fields populated (third-row seats, refrigerator
    temperature, fan/airflow settings, etc.).
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
    return HvacStatus.model_validate(decoded)
