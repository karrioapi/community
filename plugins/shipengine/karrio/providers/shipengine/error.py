"""Karrio ShipEngine error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.shipengine.utils as provider_utils


def parse_error_response(
    response: lib.Deserializable[typing.Dict],
    settings: provider_utils.Settings,
) -> typing.List[models.Message]:
    errors = lib.to_dict(response.deserialize())
    
    if "errors" in errors:
        # Handle ShipEngine error response format
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=error.get("error_code", "UNKNOWN"),
                message=error.get("message", "Unknown error"),
                details=lib.to_dict(error),
            )
            for error in errors.get("errors", [])
        ]
    
    # Handle non-standard error formats
    if "error" in errors:
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=errors.get("error", {}).get("code", "UNKNOWN"),
                message=errors.get("error", {}).get("message", "Unknown error"),
                details=lib.to_dict(errors.get("error", {})),
            )
        ]
    
    # Handle API error responses
    if "message" in errors:
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=errors.get("type", "UNKNOWN"),
                message=errors.get("message", "Unknown error"),
                details=lib.to_dict(errors),
            )
        ]
    
    return [] 
