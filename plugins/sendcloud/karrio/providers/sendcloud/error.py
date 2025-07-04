"""Karrio SendCloud error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.Message]:
    """Extract error messages from SendCloud API response."""

    errors: typing.List[models.Message] = []
    
    if "error" in response:
        error = response["error"]
        errors.append(
            models.Message(
                code=str(error.get("code", "unknown")),
                message=error.get("message", "Unknown error"),
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
            )
        )
    
    # Handle field-specific errors
    if "errors" in response:
        for field, messages in response["errors"].items():
            if isinstance(messages, list):
                for message in messages:
                    errors.append(
                        models.Message(
                            code=field,
                            message=message,
                            carrier_id=settings.carrier_id,
                            carrier_name=settings.carrier_name,
                        )
                    )
            else:
                errors.append(
                    models.Message(
                        code=field,
                        message=messages,
                        carrier_id=settings.carrier_id,
                        carrier_name=settings.carrier_name,
                    )
                )
    
    return errors 
