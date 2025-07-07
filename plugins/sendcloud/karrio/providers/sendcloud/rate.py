"""Karrio SendCloud rate API implementation."""

import karrio.schemas.sendcloud.rate_request as sendcloud
import karrio.schemas.sendcloud.rate_response as rating

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(option, settings) 
        for option in response.get("data", [])
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """Extract rate details from SendCloud multi-carrier response."""
    details = lib.to_object(rating.DatumType, data)
    
    # Create composite service ID for hub carrier pattern
    service_id = f"sendcloud_{details.carrier.code}_{details.product.code}"
    
    # Extract pricing information
    total_charge = 0.0
    currency = "EUR"
    transit_days = None
    
    if details.quotes and len(details.quotes) > 0:
        quote = details.quotes[0]
        if quote.price and quote.price.total:
            total_charge = float(quote.price.total.value or 0)
            currency = quote.price.total.currency or "EUR"
        transit_days = getattr(quote, 'leadtime', None)
    
    # Extract extra charges from breakdown
    extra_charges = []
    if details.quotes and len(details.quotes) > 0 and details.quotes[0].price:
        for breakdown in details.quotes[0].price.breakdown or []:
            if breakdown.price and float(breakdown.price.value or 0) > 0:
                extra_charges.append(
                    models.ChargeDetails(
                        name=breakdown.label,
                        amount=lib.to_money(breakdown.price.value),
                        currency=breakdown.price.currency,
                    )
                )

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service_id,
        total_charge=lib.to_money(total_charge),
        currency=currency,
        transit_days=transit_days,
        extra_charges=extra_charges,
        meta=dict(
            rate_provider=details.carrier.name,
            service_name=details.name,
            carrier_code=details.carrier.code,
            product_code=details.product.code,
            sendcloud_code=details.code,
            contract_id=details.contract.id if details.contract else None,
            # Functionalities metadata
            signature=getattr(details.functionalities, 'signature', False),
            tracked=getattr(details.functionalities, 'tracked', False),
            insurance_available=getattr(details.functionalities, 'insurance', None) is not None,
            age_check=getattr(details.functionalities, 'agecheck', None),
            delivery_deadline=getattr(details.functionalities, 'deliverydeadline', None),
            weekend_delivery=getattr(details.functionalities, 'weekenddelivery', None),
            # Weight limits
            min_weight=lib.failsafe(lambda: details.weight.min.value),
            max_weight=lib.failsafe(lambda: details.weight.max.value),
            weight_unit=lib.failsafe(lambda: details.weight.min.unit),
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a rate request for SendCloud's fetch-shipping-options API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # SendCloud expects total weight and dimensions
    total_weight = sum(pkg.weight.KG for pkg in packages)
    
    # Get max dimensions from all packages
    max_length = max((pkg.length.CM for pkg in packages if pkg.length), default=0)
    max_width = max((pkg.width.CM for pkg in packages if pkg.width), default=0) 
    max_height = max((pkg.height.CM for pkg in packages if pkg.height), default=0)

    # Map data to SendCloud rate request format
    request = sendcloud.RateRequestType(
        fromcountry=shipper.country_code,
        tocountry=recipient.country_code,
        frompostalcode=shipper.postal_code,
        topostalcode=recipient.postal_code,
        weight=total_weight,
        length=int(max_length) if max_length > 0 else None,
        width=int(max_width) if max_width > 0 else None,
        height=int(max_height) if max_height > 0 else None,
        isreturn=lib.identity(
            options.sendcloud_is_return.state 
            if options.sendcloud_is_return.state is not None
            else False
        ),
        requestlabelasync=lib.identity(
            settings.connection_config.request_label_async.state
            if settings.connection_config.request_label_async.state is not None
            else False
        ),
    )

    return lib.Serializable(request, lib.to_dict)
