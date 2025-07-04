"""Karrio SendCloud shipment creation API implementation."""

import karrio.schemas.sendcloud.shipment_request as sendcloud
import karrio.schemas.sendcloud.shipment_response as shipment

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
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    parcel = response.get("parcel") or {}
    messages = error.parse_error_response(response, settings)

    details = lib.to_object(shipment.ParcelType, parcel)
    shipment_details = models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.tracking_number,
        shipment_identifier=str(details.id),
        label=lib.identity(
            details.label.label_printer
            if details.label is not None
            else None
        ),
        docs=models.Documents(
            label=lib.identity(
                details.label.label_printer
                if details.label is not None
                else None
            ),
        ),
        meta=dict(
            sendcloud_parcel_id=details.id,
            carrier=details.carrier,
            tracking_url=details.tracking_url,
            status=details.status,
            date_created=details.date_created,
            date_updated=details.date_updated,
        ),
    )

    return shipment_details, messages


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

    # Get shipping service information
    service = provider_units.ShippingServiceID.map(payload.service)
    
    request = sendcloud.ShipmentRequestType(
        parcel=sendcloud.ParcelRequestType(
            name=recipient.person_name or "N/A",
            company_name=recipient.company_name,
            address=recipient.address_line1,
            address_2=recipient.address_line2,
            house_number=lib.identity(
                recipient.address_line1.split()[0]
                if recipient.address_line1
                else "1"
            ),
            city=recipient.city,
            postal_code=recipient.postal_code,
            country=recipient.country_code,
            telephone=recipient.phone_number,
            email=recipient.email,
            shipment=sendcloud.ShipmentType(
                id=lib.identity(
                    int(service.name_or_key.split('_')[-1])
                    if service.name_or_key and service.name_or_key.split('_')[-1].isdigit()
                    else 1
                ),
                name=service.value_or_key,
            ),
            weight=str(packages.weight.value),
            height=str(packages[0].height.value if packages else "10"),
            length=str(packages[0].length.value if packages else "10"),
            width=str(packages[0].width.value if packages else "10"),
            parcel_items=[
                sendcloud.ParcelItemType(
                    description=item.description or item.title or "Item",
                    quantity=item.quantity,
                    weight=str(item.weight or 0.1),
                    value=str(item.value_amount or 0.0),
                    sku=item.sku or "N/A",
                    hs_code=item.hs_code or "N/A",
                    origin_country=item.origin_country or shipper.country_code,
                )
                for package in packages
                for item in lib.identity(
                    package.items
                    if any(package.items)
                    else [
                        models.Commodity(
                            title=package.description or "Package",
                            description=package.description or "Package",
                            quantity=1,
                            weight=package.weight.value,
                            value_amount=1.0,
                            sku="N/A",
                            hs_code="N/A",
                        )
                    ]
                )
            ],
            customs_invoice_nr=options.sendcloud_customs_invoice_nr.state,
            customs_shipment_type=options.sendcloud_customs_shipment_type.state,
            external_order_id=options.sendcloud_external_order_id.state,
            external_shipment_id=options.sendcloud_external_shipment_id.state,
            total_order_value=options.sendcloud_total_order_value.state,
            total_order_value_currency=options.sendcloud_total_order_value_currency.state,
            is_return=options.sendcloud_is_return.state,
            insured_value=options.sendcloud_insured_value.state,
            to_service_point=lib.identity(
                int(options.sendcloud_service_point_id.state)
                if options.sendcloud_service_point_id.state
                else None
            ),
            request_label=options.sendcloud_request_label.state or True,
            request_label_async=options.sendcloud_request_label_async.state or False,
            apply_shipping_rules=options.sendcloud_apply_shipping_rules.state or False,
        )
    )

    return lib.Serializable(request, lib.to_dict) 
