"""Karrio Sendcloud error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors = response.get("error", {})
    
    if isinstance(errors, dict):
        if "message" in errors:
            return [
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=errors.get("code", "unknown"),
                    message=errors.get("message", "Unknown error"),
                    details=errors,
                )
            ]
        elif "errors" in errors:
            return [
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error.get("code", "unknown"),
                    message=error.get("message", "Unknown error"),
                    details=error,
                )
                for error in errors["errors"]
            ]
    
    if isinstance(errors, list):
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=error.get("code", "unknown"),
                message=error.get("message", "Unknown error"),
                details=error,
            )
            for error in errors
        ]
    
    if kwargs.get("status_code") and kwargs.get("status_code") != 200:
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(kwargs.get("status_code", "unknown")),
                message=response.get("message", "HTTP error"),
                details=response,
            )
        ]

    return []
