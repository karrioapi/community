"""Karrio Veho error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.veho.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors: list = []
    
    # Check for error in response
    if isinstance(response, dict) and "error" in response:
        error_data = response["error"]
        errors.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=error_data.get("code", ""),
                message=error_data.get("message", ""),
                details=dict(
                    details=error_data.get("details", ""),
                    **kwargs
                ),
            )
        )

    return errors
