"""Karrio ShipEngine error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.shipengine.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    # Extract errors from ShipEngine response
    errors = response.get("errors", [])
    
    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("error_code", ""),
            message=error.get("message", ""),
            details={
                "error_source": error.get("error_source", ""),
                "error_type": error.get("error_type", ""),
                "field_name": error.get("field_name", ""),
                "field_value": error.get("field_value", ""),
                **kwargs
            },
        )
        for error in errors
    ]
