import karrio.schemas.dhl_ecommerce_americas.rate_response as rating
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_americas.error as error
import karrio.providers.dhl_ecommerce_americas.utils as provider_utils
import karrio.providers.dhl_ecommerce_americas.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    rates_data = []
    if isinstance(response, dict):
        if "body" in response and "rates" in response["body"]:
            rates_data = response["body"]["rates"]
        elif "rates" in response:
            rates_data = response["rates"]
    elif isinstance(response, list):
        rates_data = response
    
    rates = [
        _extract_details(rate_data, settings)
        for rate_data in rates_data
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.Rate, data)
    
    extra_charges = []
    if rate.charges:
        for charge_item in rate.charges:
            if isinstance(charge_item, dict):
                charge = lib.to_object(rating.Charge, charge_item)
            else:
                charge = charge_item
            
            extra_charges.append(models.ChargeDetails(
                name=charge.chargeType or "Unknown Charge",
                currency=rate.currency or "USD",
                amount=lib.to_money(charge.chargeAmount or 0.0),
            ))

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=rate.productCode,
        total_charge=lib.to_money(rate.totalCharge or 0.0),
        currency=rate.currency or "USD",
        transit_days=rate.transitTime,
        extra_charges=extra_charges,
        meta=dict(
            service_name=rate.productName,
            product_code=rate.productCode,
            delivery_guarantee=rate.deliveryGuarantee,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = payload.services or [provider_units.ShippingService.dhl_parcel_ground.value]
    
    service_code = next(
        (provider_units.ShippingService[s].value for s in services if s in provider_units.ShippingService.__members__),
        provider_units.ShippingService.dhl_parcel_ground.value
    )

    request = {
        "consigneeAddress": {
            "postalCode": recipient.postal_code,
            "city": recipient.city,
            "state": recipient.state_code,
            "countryCode": recipient.country_code,
        },
        "consignorAddress": {
            "postalCode": shipper.postal_code,
            "city": shipper.city,
            "state": shipper.state_code,
            "countryCode": shipper.country_code,
        },
        "packages": [
            {
                "weight": package.weight.LB,
                "weightUom": "LB",
                "dimensions": {
                    "length": package.length.IN,
                    "width": package.width.IN,
                    "height": package.height.IN,
                    "dimensionUom": "IN",
                },
            }
            for package in packages
        ],
        "productCode": service_code,
        "accountNumber": getattr(settings, 'account_number', ''),
    }

    return lib.Serializable(request, lib.to_dict)
