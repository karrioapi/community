"""Karrio SendCloud error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.utils as provider_utils


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


def parse_validation_error(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.Message]:
    """
    Parse SendCloud validation errors specifically
    """
    messages = []
    
    if "error" in response and "details" in response["error"]:
        for detail in response["error"]["details"]:
            if isinstance(detail, dict) and "field" in detail:
                field = detail["field"]
                message = detail.get("message", "Validation failed")
                
                validation_error = models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=f"VALIDATION_{field.upper()}",
                    message=f"Validation error for {field}: {message}",
                    details=detail,
                )
                messages.append(validation_error)
    
    return messages


def parse_authentication_error(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.Message]:
    """
    Parse SendCloud authentication errors specifically
    """
    if "error" in response:
        error_data = response["error"]
        code = error_data.get("code", "AUTH_ERROR")
        message = error_data.get("message", "Authentication failed")
        
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(code),
                message=f"Authentication error: {message}",
                details=error_data,
            )
        ]
    
    return []
