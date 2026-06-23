"""Karrio Freightcom Rest error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.freightcom_rest.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]

    errors = [
        *[_ for _ in responses if _.get("message")],
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            message=(
                error.get("message") + ": " + "; ".join(f"{k.replace('details.', '')}: {v}" for k, v in (error.get("details", {}) or error.get("data", {})).items())
                if (error.get("details", {}) or error.get("data", {}))
                else error.get("message")
            ),
            level=_get_level(error),
            details={
                **kwargs,
                **(error.get('data', {}))
            },
        )
        for error in errors
    ]


def _get_level(error: dict, default_level: str = "error") -> str:
    """Map Freightcom error response to standardized level.
    
    Freightcom API v2 does not provide a level field in error responses.
    All error responses default to "error" level.
    """
    return default_level
