"""Karrio Freightcom Rest rate API implementation."""


import karrio.schemas.freightcom_rest.rate_request as freightcom_rest_req
import karrio.schemas.freightcom_rest.rate_response as freightcom_rest_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.freightcom_rest.error as error
import karrio.providers.freightcom_rest.utils as provider_utils
import karrio.providers.freightcom_rest.units as provider_units

import datetime

def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)

    # Extract rate objects from the response - adjust based on carrier API structure

    # For JSON APIs, find the path to rate objects
    rate_objects = response.get("rates", []) if hasattr(response, 'get') else []
    rates = [_extract_details(rate, settings) for rate in rate_objects]


    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """
    Extract rate details from carrier response data

    data: The carrier-specific rate data structure
    settings: The carrier connection settings

    Returns a RateDetails object with extracted rate information
    """
    # Convert the carrier data to a proper object for easy attribute access

    # For JSON APIs, convert dict to proper response object
    rate = lib.to_object(freightcom_rest_res.RateType, data)

    # Now access data through the object attributes
    service = provider_units.ShippingService.map(
        rate.service_id,
    )
    service_name = service.name_or_key if service else ""

    courier = provider_units.ShippingCourier.find(rate.service_id)
    rate_provider = courier.name_or_key if courier else ""

    total_obj = rate.total if hasattr(rate, 'total') else None

    total = float(int(total_obj.value) / 100) if hasattr(total_obj, 'value') and total_obj.value else 0.0
    currency = total_obj.currency if hasattr(total_obj, 'currency') else "USD"
    transit_days = int(rate.transit_time_days) if hasattr(rate, 'transit_time_days') and rate.transit_time_days else 0

    charges = [
        ("Base charge", rate.base.value, rate.base.currency),
        *((surcharge.type, surcharge.amount.value, surcharge.amount.currency) for surcharge in rate.surcharges),
        *((tax.type, tax.amount.value, tax.amount.currency) for tax in rate.taxes),
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service_name,
        total_charge=lib.to_money(total),
        currency=currency,
        transit_days=transit_days,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                currency=currency,
                amount=lib.to_money(int(amount) / 100),
            )
            for name, amount, currency in charges
            if charges
        ],
        meta=dict(
            service_name=service_name,
            rate_provider=rate_provider,
            is_rate_guaranteed=(
                rate.customs_charge_data.is_rate_guaranteed
                if hasattr(rate, 'customs_charge_data') and rate.customs_charge_data and hasattr(rate.customs_charge_data, 'is_rate_guaranteed')
                else None
            ),
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a rate request for the carrier API

    payload: The standardized RateRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Create the carrier-specific request object
    is_intl = shipper.country_code != recipient.country_code
    is_usmca_route = provider_utils.is_usmca_eligible(shipper.country_code, recipient.country_code)
    use_usmca_option = options.freightcom_use_usmca.state if "freightcom_use_usmca" in options else False
    is_usmca = is_usmca_route and use_usmca_option
    
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=packages.weight_unit,
    )

    # Use customs.commodities if available, otherwise fall back to packages.items
    commodities = customs.commodities if customs and customs.is_defined and any(customs.commodities) else packages.items

    # Only include customs for international shipments with valid customs data
    has_customs = (
        is_intl
        and customs
        and customs.is_defined
        and any(commodities)
    )

    packaging_type = provider_units.PackagingType.map(packages.package_type or "small_box").value
    ship_datetime = lib.to_next_business_datetime(
        options.shipping_date.state or datetime.datetime.now(),
        current_format="%Y-%m-%dT%H:%M",
    )

    request = freightcom_rest_req.RateRequestType(
        services=[provider_units.ShippingService.map(service).value_or_key for service in payload.services],
        excluded_services=[],
        details=freightcom_rest_req.DetailsType(
            origin=freightcom_rest_req.DestinationType(
                name=shipper.company_name or shipper.person_name,
                address=freightcom_rest_req.AddressType(
                    address_line_1=shipper.address_line1,
                    address_line_2=shipper.address_line2,
                    city=shipper.city,
                    region=shipper.state_code,
                    country=shipper.country_code,
                    postal_code=shipper.postal_code,
                ),
                residential=shipper.residential is True,
                contact_name=shipper.person_name if shipper.company_name else "",
                phone_number=freightcom_rest_req.PhoneNumberType(
                    number=shipper.phone_number,
                ) if shipper.phone_number else None,
                email_addresses=lib.join(shipper.email),
            ),
            destination=freightcom_rest_req.DestinationType(
                name=recipient.company_name or recipient.person_name,
                address=freightcom_rest_req.AddressType(
                    address_line_1=recipient.address_line1,
                    address_line_2=recipient.address_line2,
                    city=recipient.city,
                    region=recipient.state_code,
                    country=recipient.country_code,
                    postal_code=recipient.postal_code,
                ),
                residential=recipient.residential is True,
                contact_name=recipient.person_name,
                phone_number=freightcom_rest_req.PhoneNumberType(
                    number=recipient.phone_number
                ) if recipient.phone_number else None,
                email_addresses=lib.join(recipient.email),
                ready_at=freightcom_rest_req.ReadyType(
                    hour=ship_datetime.hour,
                    minute=0
                ),
                ready_until=freightcom_rest_req.ReadyType(
                    hour=17,
                    minute=0
                ),
                receives_email_updates=options.email_notification.state,
                signature_requirement="required" if options.signature_confirmation.state else "not-required"
            ),
            expected_ship_date=freightcom_rest_req.ExpectedShipDateType(
                year=ship_datetime.year,
                month=ship_datetime.month,
                day=ship_datetime.day,
            ),
            packaging_type=packaging_type,
            packaging_properties=(
                freightcom_rest_req.PackagingPropertiesType(
                pallet_type="ltl" if packaging_type == "pallet" else None,
                has_stackable_pallets=options.stackable.state if packaging_type == "pallet" else None,
                dangerous_goods=options.dangerous_goods.state,
                dangerous_goods_details=freightcom_rest_req.DangerousGoodsDetailsType(
                    packaging_group=options.dangerous_goods_group.state,
                    goods_class=options.dangerous_goods_class.state,
                ) if options.dangerous_goods.state else None,
                pallets=[
                    freightcom_rest_req.PalletType(
                        measurements=freightcom_rest_req.PackageMeasurementsType(
                            weight=freightcom_rest_req.WeightType(
                                unit="lb",
                                value=parcel.weight.LB
                            ),
                            cuboid=freightcom_rest_req.CuboidType(
                                unit="in",
                                l=parcel.length.IN,
                                w=parcel.width.IN,
                                h=parcel.height.IN
                            )
                        ),
                        description=parcel.description,
                        freight_class=options.freight_class.state,
                    ) for parcel in packages
                ] if packaging_type == "pallet" else [],
                packages=[
                    freightcom_rest_req.PackageType(
                        measurements=freightcom_rest_req.PackageMeasurementsType(
                            weight=freightcom_rest_req.WeightType(
                                unit="lb",
                                value=parcel.weight.LB
                            ),
                            cuboid=freightcom_rest_req.CuboidType(
                                unit="in",
                                l=parcel.length.IN,
                                w=parcel.width.IN,
                                h=parcel.height.IN
                            )
                        ),
                        description=parcel.description,
                    ) for parcel in packages
                ] if packaging_type == "package" else [],
                    courierpaks=[
                    freightcom_rest_req.CourierpakType(
                        measurements=freightcom_rest_req.CourierpakMeasurementsType(
                            weight=freightcom_rest_req.WeightType(
                                unit="lb",
                                value=parcel.weight.LB
                            ),
                        ),
                        description=parcel.description,
                    ) for parcel in packages
                ] if packaging_type == "courier-pak" else [],
                insurance=freightcom_rest_req.InsuranceType(
                    type='carrier',
                    total_cost=freightcom_rest_req.TotalCostType(
                        currency=options.currency.state or "CAD",
                        value=lib.to_int(options.insurance.state)
                    )
                ) if options.insurance.state else None,
                pallet_service_details=freightcom_rest_req.PalletServiceDetailsType() if packaging_type == "pallet" else None,
                )
            ),
            reference_codes=[payload.reference] if any(payload.reference or "") else [],
            customs_data=(
                freightcom_rest_req.CustomsDataType(
                    products=[
                        freightcom_rest_req.ProductType(
                            product_name=item.title,
                            weight=freightcom_rest_req.WeightType(
                                unit="kg" if item.weight_unit.upper() == "KG" else "lb",
                                value=lib.to_decimal(item.weight)
                            ),
                            hs_code=item.hs_code,
                            country_of_origin=item.origin_country,
                            num_units=item.quantity,
                            unit_price=freightcom_rest_req.TotalCostType(
                                currency=item.value_currency,
                                value=str(int(item.value_amount * 100))
                            ),
                            description=item.description,
                            fda_regulated="no",
                            cusma_included=True if is_usmca else None,
                            non_auto_parts=(
                                options.freightcom_non_auto_parts.state
                                if hasattr(options, 'freightcom_non_auto_parts') and options.freightcom_non_auto_parts.state
                                else None
                            ),
                        )
                        for item in commodities
                        if item.hs_code
                    ],
                    request_guaranteed_customs_charges=settings.connection_config.request_guaranteed_customs_charges.state or True
                )
                if has_customs
                else None
            ),
        ),
    )
    
    return lib.Serializable(request, lib.to_dict)

