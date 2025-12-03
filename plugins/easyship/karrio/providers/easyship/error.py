"""Karrio Easyship error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.easyship.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors: list = [
        *([{**response["error"], "level": "error"}] if response.get("error") else []),
        *[
            dict(code="warning", message=message, level="warning")
            for message in response.get("meta", {}).get("errors", [])
        ],
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            level=_get_level(error.get("type"), error.get("level")),
            details=lib.to_dict(
                {
                    **kwargs,
                    "details": error.get("details"),
                    "request_id": error.get("request_id"),
                    "type": error.get("type"),
                }
            ),
        )
        for error in errors
    ]


def _get_level(error_type: typing.Optional[str], default_level: str = "error") -> str:
    """Map Easyship error type to standardized level.

    Easyship uses types like: invalid_request_error, api_error, etc.
    """
    if error_type is None:
        return default_level

    error_type_lower = error_type.lower()

    # Map common error types to levels
    if "warning" in error_type_lower:
        return "warning"
    elif "info" in error_type_lower or "notice" in error_type_lower:
        return "info"

    return default_level
