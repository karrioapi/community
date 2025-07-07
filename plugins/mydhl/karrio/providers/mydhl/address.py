"""Karrio MyDHL address validation API implementation."""

import karrio.schemas.mydhl.address_validation_request as mydhl_req
import karrio.schemas.mydhl.address_validation_response as mydhl_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils


def parse_address_validation_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.AddressValidationDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    # Only create validation details if there are no errors
    validation_details = []
    if not messages:
        validation_details = [_extract_details(response, settings)]

    return validation_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.AddressValidationDetails:
    """Extract address validation details from MyDHL response."""
    validation = lib.to_object(mydhl_res.AddressValidationResponseType, data)
    
    warnings = getattr(validation, 'warnings', []) or []
    addresses = getattr(validation, 'address', []) or []
    
    return models.AddressValidationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=len(warnings) == 0,
        complete_address=models.Address(
            city=addresses[0].cityName if addresses else "",
            postal_code=addresses[0].postalCode if addresses else "",
            country_code=addresses[0].countryCode if addresses else "",
        ) if addresses else None,
    )


def address_validation_request(
    payload: models.AddressValidationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create MyDHL address validation request."""
    address = lib.to_address(payload.address)

    request = mydhl_req.AddressValidationRequestType(
        type="delivery",
        countryCode=address.country_code,
        postalCode=address.postal_code,
        cityName=address.city,
        strictValidation=True,
    )

    return lib.Serializable(request, lib.to_dict)