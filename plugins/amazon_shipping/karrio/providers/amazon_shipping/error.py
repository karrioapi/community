"""Karrio Amazon Shipping error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.amazon_shipping.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse error response from Amazon Shipping API.

    The v2 API returns errors in the format:
    {
        "errors": [
            {"code": "InvalidRequest", "message": "...", "details": "..."}
        ]
    }
    """
    errors = response.get("errors") or []

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            details={
                **kwargs,
                **({"note": error.get("details")} if error.get("details") else {}),
            } or None,
        )
        for error in errors
        if error.get("code") or error.get("message")
    ]
