"""Karrio DHL eCommerce Americas rate API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_americas.error as error
import karrio.providers.dhl_ecommerce_americas.utils as provider_utils
import karrio.providers.dhl_ecommerce_americas.units as provider_units
# CRITICAL: Always import and use the generated schema types
import karrio.schemas.dhl_ecommerce_americas.rate_request as dhl_req
import karrio.schemas.dhl_ecommerce_americas.rate_response as dhl_res

def parse_rate_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Convert to typed object using generated schema
    rate_response = lib.to_object(dhl_res.RateResponseType, response)
    
    # Extract rates using functional pattern
    rates = [
        _extract_details(lib.to_dict(rate), settings)
        for rate in (rate_response.body.rates or [])
        if rate_response.body
    ]

    return rates, messages

def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """Extract rate details from DHL response data"""

    # Convert the DHL data to a proper object for easy attribute access
    rate = lib.to_object(dhl_res.RateType, data)

    # Functional calculation of extra charges
    extra_charges = [
        models.ChargeDetails(
            name=charge.chargeType or "Unknown Charge",
            currency=rate.currency or "USD",
            amount=lib.to_money(charge.chargeAmount or 0.0),
        )
        for charge in (rate.charges or [])
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=rate.productCode if hasattr(rate, 'productCode') else "",
        total_charge=lib.to_money(rate.totalCharge),
        currency=rate.currency if hasattr(rate, 'currency') else "USD",
        transit_days=int(rate.transitTime) if hasattr(rate, 'transitTime') and rate.transitTime else None,
        extra_charges=extra_charges,
        meta=dict(
            service_name=rate.productName if hasattr(rate, 'productName') else "",
            product_code=rate.productCode if hasattr(rate, 'productCode') else "",
            delivery_guarantee=rate.deliveryGuarantee if hasattr(rate, 'deliveryGuarantee') else False,
        ),
    )

def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a rate request for the DHL eCommerce Americas API"""

    # Convert karrio models to DHL-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    
    # Handle service selection
    services = payload.services or [provider_units.ShippingService.dhl_parcel_ground.value]
    service_code = next(
        (provider_units.ShippingService[s].value for s in services if s in provider_units.ShippingService.__members__),
        provider_units.ShippingService.dhl_parcel_ground.value
    )

    # Create the DHL-specific request object using generated types
    request = dhl_req.RateRequestType(
        consigneeAddress=dhl_req.ConsigneeAddressType(
            postalCode=recipient.postal_code,
            city=recipient.city,
            state=recipient.state_code,
            countryCode=recipient.country_code,
        ),
        consignorAddress=dhl_req.ConsignorAddressType(
            postalCode=shipper.postal_code,
            city=shipper.city,
            state=shipper.state_code,
            countryCode=shipper.country_code,
        ),
        packages=[
            dhl_req.PackageType(
                weight=package.weight.LB,  # DHL Americas uses LB
                weightUom="LB",
                dimensions=dhl_req.DimensionsType(
                    length=package.length.IN if package.length else None,
                    width=package.width.IN if package.width else None,
                    height=package.height.IN if package.height else None,
                    dimensionUom="IN",
                ) if all([package.length, package.width, package.height]) else None,
            )
            for package in packages
        ],
        productCode=service_code,
        accountNumber=getattr(settings, 'account_number', ''),
    )

    return lib.Serializable(request, lib.to_dict)