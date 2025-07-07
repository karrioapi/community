"""Karrio SendCloud error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.utils as provider_utils
import karrio.schemas.sendcloud.error as error_schemas


def parse_error_response(
    response: typing.Union[dict, list],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors: typing.List[models.Message] = []
    
    # Handle dict response
    if isinstance(response, dict):
        # Check for error field
        if "error" in response:
            error_data = response["error"]
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error_data.get("code", "UNKNOWN"),
                    message=error_data.get("message", "Unknown error occurred"),
                    details={
                        "details": error_data.get("details", ""),
                    },
                )
            )
        
        # Check for validation errors field
        if "errors" in response and isinstance(response["errors"], dict):
            for field, messages in response["errors"].items():
                for message in messages if isinstance(messages, list) else [messages]:
                    errors.append(
                        models.Message(
                            carrier_id=settings.carrier_id,
                            carrier_name=settings.carrier_name,
                            code="VALIDATION_ERROR",
                            message=f"{field}: {message}",
                            details={**kwargs, "field": field},
                        )
                    )
        
        # Check for simple message field (common in APIs)
        if not errors and "message" in response:
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=response.get("code", "ERROR"),
                    message=response["message"],
                    details={**kwargs},
                )
            )
    
    # Handle list response (batch errors)
    elif isinstance(response, list):
        for idx, error in enumerate(response):
            if isinstance(error, dict):
                errors.append(
                    models.Message(
                        carrier_id=settings.carrier_id,
                        carrier_name=settings.carrier_name,
                        code=error.get("code", "ERROR"),
                        message=error.get("message", f"Error at index {idx}"),
                        details={**kwargs, "index": idx},
                    )
                )

    return errors
