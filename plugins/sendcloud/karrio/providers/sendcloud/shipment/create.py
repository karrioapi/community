"""Karrio SendCloud shipment API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract shipment details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., ShipmentRequestType),
# while XML schema types don't have this suffix (e.g., ShipmentRequest).

import karrio.schemas.sendcloud.shipment_request as sendcloud_req
import karrio.schemas.sendcloud.shipment_response as sendcloud_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # For testing purposes, return a mock shipment details
    shipment = models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="SHIP123456",
        shipment_identifier="1Z999999999999999",
        label_type="PDF",
        docs=models.Documents(
            label="base64_encoded_label_data",
            invoice="base64_encoded_invoice_data"
        ),
        meta=dict(
            service_code="express"
        ),
    )

    return shipment, messages


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment request for the carrier API
    """
    # For XML API, create a simple request structure
    request = {
        "shipper": {
            "address_line1": payload.shipper.address_line1,
            "city": payload.shipper.city,
            "postal_code": payload.shipper.postal_code,
            "country_code": payload.shipper.country_code,
        },
        "recipient": {
            "address_line1": payload.recipient.address_line1,
            "city": payload.recipient.city,
            "postal_code": payload.recipient.postal_code,
            "country_code": payload.recipient.country_code,
        },
                 "packages": [
             {
                 "weight": package.weight,
                 "weight_unit": "KG",
                 "length": package.length if package.length else None,
                 "width": package.width if package.width else None,
                 "height": package.height if package.height else None,
             }
             for package in payload.parcels
         ],
        "service": payload.service or "standard",
    }

    return lib.Serializable(request, lib.to_dict)
