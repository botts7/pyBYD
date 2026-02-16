"""Sentry (sentinel) mode control endpoint.

Endpoint:
  - /control/remoteControlPreSentinel (trigger)

Sentry mode uses the remote control pattern.  The command type is
``PRESENTINEL`` and the sentry state is toggled via ``controlParamsMap``
with ``{"sentrySwitch": "1"}`` or ``{"sentrySwitch": "0"}``.

The current sentry status is readable from realtime data as
``sentryStatus`` (0=off, 1=on, 2=triggered).
"""

from __future__ import annotations

import logging
from typing import Any

from pybyd._api._common import ENDPOINT_NOT_SUPPORTED_CODES, build_inner_base, post_token_json
from pybyd._crypto.hashing import md5_hex
from pybyd._transport import Transport
from pybyd.config import BydConfig
from pybyd.exceptions import BydControlPasswordError
from pybyd.models.sentry import SentryModeResult
from pybyd.session import Session

_logger = logging.getLogger(__name__)

_ENDPOINT = "/control/remoteControlPreSentinel"
_PASSWORD_ERROR_CODES: frozenset[str] = frozenset({"5005", "5006"})


async def trigger_sentry_mode(
    config: BydConfig,
    session: Session,
    transport: Transport,
    vin: str,
    *,
    enable: bool,
    command_pwd: str,
) -> SentryModeResult:
    """Trigger sentry mode on or off.

    .. warning::
        This endpoint is untested on a vehicle that supports sentry mode.
        It returned ``1009`` (not supported) on AU region during probing.
        Requires the user's remote control PIN set in the BYD app.

    Parameters
    ----------
    enable
        ``True`` to arm sentry, ``False`` to disarm.
    command_pwd
        The vehicle control password (plaintext, user-set in BYD app).
    """
    inner = build_inner_base(config, vin=vin)
    inner["commandType"] = "PRESENTINEL"
    inner["controlParamsMap"] = '{"sentrySwitch": "' + ("1" if enable else "0") + '"}'
    inner["commandPassword"] = md5_hex(command_pwd)

    decoded = await post_token_json(
        endpoint=_ENDPOINT,
        config=config,
        session=session,
        transport=transport,
        inner=inner,
        vin=vin,
        not_supported_codes=ENDPOINT_NOT_SUPPORTED_CODES,
        extra_code_map={_PASSWORD_ERROR_CODES: BydControlPasswordError},
    )
    return _parse_result(decoded, enable=enable)


def _parse_result(data: Any, *, enable: bool) -> SentryModeResult:
    """Parse sentry trigger response."""
    success = False
    if isinstance(data, dict):
        control_state = data.get("controlState")
        success = control_state in (1, "1", "SUCCESS")
    return SentryModeResult(success=success, sentry_enabled=enable)
