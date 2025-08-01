"""Karrio GLS EU pickup API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls_eu.error as error


def parse_pickup_response(
    _response: lib.Deserializable,
    settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    pickup = models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=response.get("pickupId", ""),
        pickup_date=response.get("pickupDate"),
        pickup_charge=models.ChargeDetails(
            name="Pickup",
            amount=response.get("charge", 0.0),
            currency="EUR"
        ),
    )

    return pickup, messages


def pickup_request(
    payload: models.PickupRequest,
    settings,
) -> lib.Serializable:
    request = {
        "pickupDate": payload.pickup_date,
        "address": {
            "street": payload.address.address_line1,
            "city": payload.address.city,
            "postalCode": payload.address.postal_code,
            "country": payload.address.country_code,
        },
        "timeWindow": {
            "start": payload.ready_time,
            "end": payload.closing_time,
        },
        "packages": [
            {
                "weight": package.weight.value,
                "reference": package.packaging_type or "package"
            }
            for package in payload.parcels
        ]
    }

    return lib.Serializable(request, lib.to_dict)
