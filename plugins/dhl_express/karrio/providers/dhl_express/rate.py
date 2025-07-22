from typing import Tuple, List
import datetime
from karrio.core.utils import Serializable, Deserializable, SF
from karrio.core.models import RateRequest, RateDetails, Message
from karrio.providers.dhl_express.error import parse_error_response
from karrio.providers.dhl_express.utils import Settings, request
import karrio.providers.dhl_express.units as provider_units
import karrio.lib as lib


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[List[RateDetails], List[Message]]:
    response = _response.deserialize()
    messages: List[Message] = parse_error_response(response, settings)
    rates: List[RateDetails] = []

    if "products" in response:
        rates = [
            _extract_details(product, settings)
            for product in response["products"]
        ]

    return rates, messages


def _extract_details(product: dict, settings: Settings) -> RateDetails:
    service = product.get("productName")
    charges = product.get("totalPrice", [])
    currency = charges[0].get("currencyType") if charges else "USD"
    total_charge = sum(float(charge.get("price", 0)) for charge in charges)
    
    return RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service,
        total_charge=lib.to_decimal(total_charge),
        currency=currency,
        transit_days=product.get("deliveryCapabilities", {}).get("totalTransitDays"),
        extra_charges=[
            lib.ChargeDetails(
                name=charge.get("serviceTypeCode", ""),
                amount=lib.to_decimal(charge.get("price", 0)),
                currency=charge.get("currencyType", currency),
            )
            for charge in charges[1:]  # Skip the first one which is the base price
        ],
        meta=dict(
            service_type=product.get("productCode"),
        ),
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable:
    """Create rate request for DHL Express."""
    
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    
    packages = lib.to_packages(payload.parcels)
    package = packages[0]
    
    request_data = {
        "plannedShippingDateAndTime": lib.fdatetime(
            options.shipment_date.state or datetime.datetime.now(),
            output_format="%Y-%m-%dT%H:%M:%S"
        ),
        "pickup": {
            "isRequested": False
        },
        "productCode": getattr(payload, "service", "EXPRESS_WORLDWIDE"),
        "accounts": [
            {
                "typeCode": "shipper",
                "number": settings.account_number
            }
        ] if settings.account_number else [],
        "customerDetails": {
            "shipperDetails": {
                "postalAddress": {
                    "postalCode": payload.shipper.postal_code,
                    "cityName": payload.shipper.city,
                    "countryCode": payload.shipper.country_code,
                    "addressLine1": payload.shipper.address_line1 or "",
                }
            },
            "receiverDetails": {
                "postalAddress": {
                    "postalCode": payload.recipient.postal_code,
                    "cityName": payload.recipient.city,
                    "countryCode": payload.recipient.country_code,
                    "addressLine1": payload.recipient.address_line1 or "",
                }
            }
        },
        "packages": [
            {
                "weight": package.weight.value,
                "dimensions": {
                    "length": package.length.value,
                    "width": package.width.value,
                    "height": package.height.value,
                },
            }
        ],
    }
    
    return Serializable(request_data, lib.to_dict)


def get_rates(payload: RateRequest, settings: Settings) -> Deserializable[str]:
    """Get rates from DHL Express."""
    
    request_data = rate_request(payload, settings)
    response = request(
        url=f"{settings.server_url}/rates",
        data=request_data.serialize(),
        trace=payload.reference,
        method="POST",
        settings=settings,
    )
    
    return Deserializable(response, lib.to_dict)
