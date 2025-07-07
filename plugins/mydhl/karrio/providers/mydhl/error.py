"""Karrio MyDHL error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.utils as provider_utils

def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse MyDHL error responses."""

    # Handle standard error response format
    if "detail" in response:
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=response.get("status", ""),
                message=response.get("detail", ""),
                details=dict(
                    instance=response.get("instance", ""),
                    title=response.get("title", ""),
                    **kwargs
                ),
            )
        ]

    # Handle error object format
    if "error" in response:
        error = response["error"]
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=error.get("code", ""),
                message=error.get("message", ""),
                details=dict(
                    details=error.get("details", ""),
                    **kwargs
                ),
            )
        ]

    # Handle additional error formats if present
    errors = response.get("errors", [])
    additional_details = response.get("additionalDetails", [])

    messages = []

    # Process main errors
    for error in errors:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=error.get("code", ""),
                message=error.get("message", ""),
                details=dict(error, **kwargs),
            )
        )

    # Process additional validation errors
    for detail in additional_details:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="validation_error",
                message=detail,
                details=dict(validation_detail=detail, **kwargs),
            )
        )

    return messages