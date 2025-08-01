"""Karrio MyDHL error parsing."""

import typing
import karrio.lib as lib
import karrio.core.models as models


def parse_error_response(
    response: dict,
    settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse MyDHL API error response into Karrio error messages."""
    
    errors = response.get("errors", [])
    messages = []
    
    if not errors and response.get("error"):
        # Single error format
        error = response.get("error", {})
        messages.append(
            models.Message(
                code=error.get("code", "UNKNOWN"),
                message=error.get("message", "Unknown error occurred"),
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
            )
        )
    else:
        # Multiple errors format
        for error in errors:
            messages.append(
                models.Message(
                    code=error.get("code", "UNKNOWN"),
                    message=error.get("message", "Unknown error occurred"),
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                )
            )
    
    return messages
