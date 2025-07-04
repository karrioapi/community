"""Karrio ShipEngine shipment creation parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.core.units as units
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils
import karrio.providers.shipengine.units as provider_units


def parse_shipment_response(
    response: lib.Deserializable[typing.Dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.ShipmentDetails], typing.List[models.Message]]:
    responses = lib.to_dict(response.deserialize())
    messages = error.parse_error_response(response, settings)
    
    shipment_details = [
        _extract_details(responses, settings)
    ] if "label_id" in responses else []
    
    return shipment_details, messages


def _extract_details(
    data: typing.Dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_dict(data)
    
    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.get("tracking_number"),
        shipment_identifier=shipment.get("shipment_id"),
        label_type="PDF",
        docs=models.Documents(
            label=shipment.get("label_download", {}).get("pdf") or shipment.get("label_download", {}).get("href"),
        ),
        meta=dict(
            label_id=shipment.get("label_id"),
            service_code=shipment.get("service_code"),
            carrier_code=shipment.get("carrier_code"),
            carrier_id=shipment.get("carrier_id"),
            ship_date=shipment.get("ship_date"),
            created_at=shipment.get("created_at"),
            shipment_cost=shipment.get("shipment_cost"),
            insurance_cost=shipment.get("insurance_cost"),
            is_return_label=shipment.get("is_return_label"),
            is_international=shipment.get("is_international"),
            label_format=shipment.get("label_format"),
            label_layout=shipment.get("label_layout"),
            display_scheme=shipment.get("display_scheme"),
            trackable=shipment.get("trackable"),
            **shipment,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    
    # Get preferred service
    service_code = payload.selected_rate_id or getattr(options, "shipengine_service_code", None)
    carrier_id = getattr(options, "shipengine_carrier_id", None)
    
    # Get label preferences
    label_format = getattr(options, "shipengine_label_format", "pdf")
    label_layout = getattr(options, "shipengine_label_layout", "4x6")
    display_scheme = getattr(options, "shipengine_display_scheme", "label")
    validate_address = getattr(options, "shipengine_validate_address", "no_validation")
    
    # Build advanced options
    advanced_options = dict()
    
    if getattr(options, "shipengine_saturday_delivery", False):
        advanced_options["saturday_delivery"] = True
    if getattr(options, "shipengine_non_machinable", False):
        advanced_options["non_machinable"] = True
    if getattr(options, "shipengine_contains_alcohol", False):
        advanced_options["contains_alcohol"] = True
    if getattr(options, "shipengine_delivered_duty_paid", False):
        advanced_options["delivered_duty_paid"] = True
    if getattr(options, "shipengine_dry_ice", False):
        advanced_options["dry_ice"] = True
        dry_ice_weight = getattr(options, "shipengine_dry_ice_weight", None)
        if dry_ice_weight:
            advanced_options["dry_ice_weight"] = dict(
                value=float(dry_ice_weight),
                unit="pound",
            )
    
    # Build billing options
    bill_to_account = getattr(options, "shipengine_bill_to_account", None)
    bill_to_country_code = getattr(options, "shipengine_bill_to_country_code", None)
    bill_to_party = getattr(options, "shipengine_bill_to_party", None)
    bill_to_postal_code = getattr(options, "shipengine_bill_to_postal_code", None)
    
    if bill_to_account:
        advanced_options["bill_to_account"] = bill_to_account
    if bill_to_country_code:
        advanced_options["bill_to_country_code"] = bill_to_country_code
    if bill_to_party:
        advanced_options["bill_to_party"] = bill_to_party
    if bill_to_postal_code:
        advanced_options["bill_to_postal_code"] = bill_to_postal_code
    
    # Build freight options
    freight_class = getattr(options, "shipengine_freight_class", None)
    freight_charge = getattr(options, "shipengine_freight_charge", None)
    
    if freight_class:
        advanced_options["freight_class"] = freight_class
    if freight_charge:
        advanced_options["freight_charge"] = dict(
            amount=float(freight_charge),
            currency=units.Currency.map(payload.options.get("currency") or "USD").value,
        )
    
    # Build COD options
    cod_payment_type = getattr(options, "shipengine_cod_payment_type", None)
    cod_payment_amount = getattr(options, "shipengine_cod_payment_amount", None)
    
    if cod_payment_type and cod_payment_amount:
        advanced_options["collect_on_delivery"] = dict(
            payment_type=cod_payment_type,
            payment_amount=dict(
                amount=float(cod_payment_amount),
                currency=units.Currency.map(payload.options.get("currency") or "USD").value,
            ),
        )
    
    # Build customs for international shipments
    customs = None
    if payload.customs:
        customs = dict(
            contents=payload.customs.content_type or "merchandise",
            non_delivery=payload.customs.options.get("non_delivery", "return_to_sender"),
            customs_items=[
                dict(
                    customs_item_id=item.sku,
                    description=item.description,
                    quantity=item.quantity,
                    value=dict(
                        amount=float(item.value_amount),
                        currency=item.value_currency,
                    ),
                    harmonized_tariff_code=item.hs_code,
                    country_of_origin=item.origin_country,
                    unit_of_measure=item.metadata.get("unit_of_measure", "each"),
                    sku=item.sku,
                )
                for item in payload.customs.commodities
            ],
        )
    
    request = dict(
        shipment=dict(
            service_code=service_code,
            ship_to=dict(
                name=recipient.person_name or recipient.company_name,
                company_name=recipient.company_name,
                address_line1=recipient.address_line1,
                address_line2=recipient.address_line2,
                city_locality=recipient.city,
                state_province=recipient.state_code,
                postal_code=recipient.postal_code,
                country_code=recipient.country_code,
                phone=recipient.phone_number,
                email=recipient.email,
                address_residential_indicator="yes" if recipient.residential else "no",
            ),
            ship_from=dict(
                name=shipper.person_name or shipper.company_name,
                company_name=shipper.company_name,
                address_line1=shipper.address_line1,
                address_line2=shipper.address_line2,
                city_locality=shipper.city,
                state_province=shipper.state_code,
                postal_code=shipper.postal_code,
                country_code=shipper.country_code,
                phone=shipper.phone_number,
                email=shipper.email,
                address_residential_indicator="yes" if shipper.residential else "no",
            ),
            packages=[
                dict(
                    weight=dict(
                        value=float(package.weight.value),
                        unit=package.weight.unit.lower(),
                    ),
                    dimensions=dict(
                        length=float(package.length.value),
                        width=float(package.width.value),
                        height=float(package.height.value),
                        unit=package.dimension_unit.lower(),
                    ),
                    package_code=getattr(package, "packaging_type", None),
                    insured_value=dict(
                        amount=float(package.options.get("insurance", 0) or 0),
                        currency=units.Currency.map(payload.options.get("currency") or "USD").value,
                    ) if package.options.get("insurance") else None,
                    label_messages=dict(
                        reference1=getattr(options, "shipengine_reference1", None) or payload.reference,
                        reference2=getattr(options, "shipengine_reference2", None),
                        reference3=getattr(options, "shipengine_reference3", None),
                    ),
                    external_package_id=package.parcel.reference,
                )
                for package in packages
            ],
            customs=customs,
            advanced_options=advanced_options if advanced_options else None,
        ),
        rate_id=payload.selected_rate_id if payload.selected_rate_id and payload.selected_rate_id != service_code else None,
        validate_address=validate_address,
        label_layout=label_layout,
        label_format=label_format,
        display_scheme=display_scheme,
    )
    
    return lib.Serializable(request) 
