"""Karrio SendCloud error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.Message]:
    errors = []
    
    if "error" in response:
        error_data = response["error"]
        
        if isinstance(error_data, dict):
            message = error_data.get("message", "Unknown error")
            code = error_data.get("code", "UNKNOWN")
            
            errors.append(
                models.Message(
                    code=code,
                    message=message,
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    details=lib.to_dict(error_data),
                )
            )
        elif isinstance(error_data, str):
            errors.append(
                models.Message(
                    code="ERROR",
                    message=error_data,
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                )
            )
    
    elif "errors" in response:
        error_list = response["errors"]
        for error in error_list:
            if isinstance(error, dict):
                message = error.get("message", "Unknown error")
                code = error.get("code", "UNKNOWN")
                field = error.get("field", "")
                
                errors.append(
                    models.Message(
                        code=code,
                        message=f"{field}: {message}" if field else message,
                        carrier_id=settings.carrier_id,
                        carrier_name=settings.carrier_name,
                        details=lib.to_dict(error),
                    )
                )
    
    elif "message" in response:
        errors.append(
            models.Message(
                code="ERROR",
                message=response["message"],
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
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
