"""Scheduled actions / bookings endpoint.

Endpoint:
  - /control/getBookingList
"""

from __future__ import annotations

from typing import Any

from pybyd._api._common import ENDPOINT_NOT_SUPPORTED_CODES, build_inner_base, post_token_json
from pybyd._transport import Transport
from pybyd.config import BydConfig
from pybyd.session import Session

_ENDPOINT = "/control/getBookingList"


async def fetch_bookings(
    config: BydConfig,
    session: Session,
    transport: Transport,
    vin: str,
) -> list[dict[str, Any]]:
    """Fetch scheduled actions / bookings for a vehicle.

    Returns the raw decoded response as a list of booking dicts.
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
    if isinstance(decoded, list):
        return decoded
    if isinstance(decoded, dict):
        return decoded.get("list") or decoded.get("bookingList") or []
    return []
