"""Karrio ShipEngine address validation API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract address validation details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., AddressValidationRequestType),
# while XML schema types don't have this suffix (e.g., AddressValidationRequest).

import karrio.schemas.shipengine.address_validation_request as shipengine_req
import karrio.schemas.shipengine.address_validation_response as shipengine_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils
import karrio.providers.shipengine.units as provider_units


def parse_address_validation_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.AddressValidationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    validation_response = lib.to_object(shipengine_res.AddressValidationResponseType, response)

    complete_address = lib.identity(
        models.Address(
            address_line1=validation_response.normalized_address.street_address or "",
            city=validation_response.normalized_address.city_locality or "",
            postal_code=str(validation_response.normalized_address.postal_code) if validation_response.normalized_address.postal_code else "",
            country_code=validation_response.normalized_address.country_code or "",
            state_code=validation_response.normalized_address.state_province or "",
        )
        if validation_response.normalized_address else None
    )

    return models.AddressValidationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=validation_response.is_valid or False,
        complete_address=complete_address,
    ), messages


def address_validation_request(
    payload: models.AddressValidationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    address = lib.to_address(payload.address)

    request = shipengine_req.AddressValidationRequestType(
        street_address=address.address_line1 or "",
        city_locality=address.city or "",
        postal_code=lib.failsafe(lambda: int(address.postal_code)) if address.postal_code and address.postal_code.isdigit() else None,
        country_code=address.country_code or "",
        state_province=address.state_code or "",
    )

    return lib.Serializable(request, lib.to_dict)