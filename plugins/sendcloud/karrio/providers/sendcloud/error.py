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
    """Parse SendCloud API error response following established Karrio patterns."""
    
    # Extract errors from various possible response structures
    errors = []
    
    # Handle standard error structure
    if "error" in response:
        error = response["error"]
        if isinstance(error, dict):
            errors.append(error)
        elif isinstance(error, str):
            errors.append({"message": error})
    
    # Handle errors array
    if "errors" in response:
        error_list = response["errors"]
        if isinstance(error_list, list):
            errors.extend(error_list)
        elif isinstance(error_list, dict):
            errors.append(error_list)
    
    # Handle message field
    if "message" in response and not errors:
        errors.append({"message": response["message"]})
    
    # Handle detail field (common in DRF APIs)
    if "detail" in response and not errors:
        errors.append({"message": response["detail"]})
        
    # Handle validation errors
    if "non_field_errors" in response:
        for error in response["non_field_errors"]:
            errors.append({"message": error})
    
    # Handle field-specific errors
    for field, field_errors in response.items():
        if field not in ["error", "errors", "message", "detail", "non_field_errors"] and isinstance(field_errors, list):
            for error in field_errors:
                errors.append({"message": f"{field}: {error}", "field": field})

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=lib.failsafe(lambda: error.get("code") or error.get("error_code") or "SENDCLOUD_ERROR"),
            message=lib.failsafe(lambda: error.get("message") or error.get("error_message") or str(error)),
            details=lib.to_dict(
                {
                    "field": error.get("field"),
                    "error_type": error.get("type"),
                    "response": response,
                    **kwargs,
                }
            ),
        )
        for error in errors
    ]
