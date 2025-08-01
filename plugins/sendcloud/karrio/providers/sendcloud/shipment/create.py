"""Karrio Sendcloud shipment API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.ShipmentDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = lib.identity(
        _extract_details(response, settings, ctx=_response.ctx)
        if response.get("parcel")
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    parcel = data.get("parcel", {})
    tracking_number = parcel.get("tracking_number")
    parcel_id = parcel.get("id")
    
    label_url = parcel.get("label", {}).get("label_printer")
    label_content = None
    label_type = "PDF"
    
    if label_url:
        label_content = label_url
        label_type = "url"

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=str(parcel_id),
        label_type=label_type,
        docs=models.Documents(
            label=label_content if label_content else None
        ),
        meta=dict(
            parcel_id=parcel_id,
            tracking_number=tracking_number,
            service_point=parcel.get("service_point"),
            carrier=parcel.get("carrier"),
            label_url=label_url,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, options=payload.options)
    
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
    )

    total_weight = sum(
        package.weight.value * (1000 if package.weight.unit == "KG" else 1)
        for package in packages
    )

    request = {
        "parcel": {
            "name": recipient.person_name or recipient.company_name or "Customer",
            "company_name": recipient.company_name or "",
            "address": recipient.address_line1,
            "address_2": recipient.address_line2 or "",
            "city": recipient.city,
            "postal_code": recipient.postal_code,
            "country": recipient.country_code,
            "telephone": recipient.phone_number or "",
            "email": recipient.email or "",
            "weight": str(int(total_weight)),
            "order_number": options.sendcloud_order_number.state or payload.reference or "",
            "parcel_items": [
                {
                    "description": item.description or item.title or "Item",
                    "quantity": item.quantity or 1,
                    "weight": str(int(item.weight.value * (1000 if item.weight.unit == "KG" else 1))) if item.weight else "100",
                    "value": str(item.value_amount or 1.0),
                    "hs_code": item.hs_code or "",
                    "origin_country": item.origin_country or shipper.country_code,
                }
                for package in packages
                for item in (package.items or [models.Commodity(
                    title="Package",
                    description=package.description or "Package",
                    quantity=1,
                    weight=package.weight.value,
                    value_amount=1.0,
                )])
            ],
        }
    }

    if options.sendcloud_service_point_id.state:
        request["parcel"]["service_point_id"] = options.sendcloud_service_point_id.state

    if options.sendcloud_require_signature.state:
        request["parcel"]["require_signature"] = options.sendcloud_require_signature.state

    if options.sendcloud_insured_value.state:
        request["parcel"]["insured_value"] = options.sendcloud_insured_value.state

    if options.sendcloud_reference.state:
        request["parcel"]["reference"] = options.sendcloud_reference.state

    if payload.service:
        request["parcel"]["shipping_method"] = payload.service

    if customs and customs.duty:
        request["parcel"]["customs_declaration"] = {
            "contents": options.sendcloud_contents.state or customs.content_type or "goods",
            "invoice_nr": options.sendcloud_customs_invoice_nr.state or "",
            "non_delivery": "return",
            "shipment_type": options.sendcloud_customs_shipment_type.state or "commercial_goods",
        }

    return lib.Serializable(request, lib.to_dict)
