"""Karrio Freightcom Rest shipment API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract shipment details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., ShipmentRequestType),
# while XML schema types don't have this suffix (e.g., ShipmentRequest).

import karrio.schemas.freightcom_rest.shipment_request as freightcom_rest_req
import karrio.schemas.freightcom_rest.shipment_response as freightcom_rest_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.freightcom_rest.error as error
import karrio.providers.freightcom_rest.utils as provider_utils
import karrio.providers.freightcom_rest.units as provider_units

import datetime
import uuid


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if we have valid shipment data

    has_shipment = "shipment" in response if hasattr(response, 'get') else False

    shipment = _extract_details(response, settings, ctx=_response._ctx) if has_shipment else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    """
    Extract shipment details from carrier response data

    data: The carrier-specific shipment data structure
    settings: The carrier connection settings

    Returns a ShipmentDetails object with extracted shipment information
    """
    # Convert the carrier data to a proper object for easy attribute access

    # For JSON APIs, convert dict to proper response object
    response_obj = lib.to_object(freightcom_rest_res.ShipmentResponseType, data)

    # Access the shipment data
    shipment = response_obj.shipment if hasattr(response_obj, 'shipment') else None

    if shipment:
        # Extract tracking info
        tracking_number = shipment.primary_tracking_number if hasattr(shipment, 'primary_tracking_number') else ""
        shipment_id = shipment.id if hasattr(shipment, 'id') else ""

        # Extract label info
        label_format = "ZPL" if ctx.get("label_type") == "ZPL" else "PDF"

        label_url = [_.url for _ in shipment.labels if
                     _.format == label_format.lower() and _.size == "a6" and not _.padded]
        label_base64 = provider_utils.download_document_to_base64(label_url[0]) if label_url else ""

        # Extract optional invoice
        customers_invoice_url = shipment.customs_invoice_url if hasattr(shipment, 'customs_invoice_url') else ""
        invoice_base64 = provider_utils.download_document_to_base64(shipment.customs_invoice_url) if customers_invoice_url else ""

        # Extract service code for metadata
        # service_code = shipment.serviceCode if hasattr(shipment, 'serviceCode') else ""

        tracking_numbers = (
            ([shipment.primary_tracking_number] if hasattr(shipment, "primary_tracking_number") else []) +
            [
                tn for tn in shipment.tracking_numbers
                if hasattr(shipment, "primary_tracking_number") and tn != shipment.primary_tracking_number
            ]
        )

        rate = shipment.rate
        service = provider_units.ShippingService.map(
            rate.service_id,
        )
        service_name = service.name_or_key
        courier = provider_units.ShippingCourier.find(rate.service_id)

        rate_provider = courier.name_or_key
        carrier_tracking_link = shipment.tracking_url if hasattr(shipment, 'tracking_url') else ""

        freightcom_service_id = rate.service_id if hasattr(rate, 'service_id') else ""
        freightcom_unique_id = shipment.unique_id if hasattr(shipment, 'unique_id') else ""

    else:
        tracking_number = ""
        shipment_id = ""
        label_format = "PDF"
        label_base64 = ""
        invoice_base64 = ""
        # service_code = ""

        #  added
        tracking_numbers = ""
        service_name = ""
        rate_provider = ""
        carrier_tracking_link = ""
        freightcom_service_id = ""
        freightcom_unique_id = ""

    documents = models.Documents(
        label=label_base64,
    )

    # Add invoice if present
    if invoice_base64:
        documents.invoice = invoice_base64

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_id,
        label_type=label_format,
        docs=documents,
        meta=dict(
            # service_code=service_code,
            carrier_tracking_link=carrier_tracking_link,
            tracking_numbers=tracking_numbers,
            rate_provider=rate_provider,
            service_name=service_name,
            freightcom_service_id=freightcom_service_id,
            freightcom_unique_id=freightcom_unique_id,
            freightcom_shipment_identifier=shipment_id
        ),
    )



def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment request for the carrier API

    payload: The standardized ShipmentRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Create the carrier-specific request object
    packaging_type = provider_units.PackagingType.map(
        packages.package_type or "small_box"
    ).value

    ship_datetime = lib.to_next_business_datetime(
        options.shipping_date.state or datetime.datetime.now(),
        current_format="%Y-%m-%dT%H:%M",
    )

    is_intl = shipper.country_code != recipient.country_code
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=packages.weight_unit,
        default_to=(
            models.Customs(
                commodities=(
                    packages.items
                    if any(packages.items)
                    else [
                        models.Commodity(
                            quantity=1,
                            sku=f"000{index}",
                            weight=pkg.weight.value,
                            weight_unit=pkg.weight_unit.value,
                            description=pkg.parcel.content,
                        )
                        for index, pkg in enumerate(packages, start=1)
                    ]
                )
            )
            if is_intl
            else None
        ),
    )

    payment_method_id = settings.payment_method

    if not payment_method_id:
        raise Exception("No payment method found need to be set in config")

    request = freightcom_rest_req.ShipmentRequestType(
        unique_id=str(uuid.uuid4()),
        payment_method_id=payment_method_id,
        service_id=provider_units.ShippingService.map(payload.service).value_or_key,
        details=freightcom_rest_req.ShipmentRequestDetailsType(
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
                phone_number=freightcom_rest_req.NumberType(
                    number=shipper.phone_number
                ) if shipper.phone_number else None,
                email_addresses=[shipper.email] if shipper.email else [],
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
                phone_number=freightcom_rest_req.NumberType(
                    number=recipient.phone_number
                ) if recipient.phone_number else None,
                email_addresses=[recipient.email] if recipient.email else [],
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
            expected_ship_date=freightcom_rest_req.DateType(
                year=ship_datetime.year,
                month=ship_datetime.month,
                day=ship_datetime.day,
            ),
            packaging_type=packaging_type,
            packaging_properties=freightcom_rest_req.PackagingPropertiesType(
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
                                unit="kg",
                                value=parcel.weight.KG
                            ),
                            cuboid=freightcom_rest_req.CuboidType(
                                unit="cm",
                                l=parcel.length.CM,
                                w=parcel.width.CM,
                                h=parcel.height.CM
                            )
                        ),
                        description=parcel.description or "N/A",
                        freight_class=options.freight_class.state,
                    ) for parcel in packages
                ] if packaging_type == "pallet" else [],
                packages=[
                    freightcom_rest_req.PackageType(
                        measurements=freightcom_rest_req.PackageMeasurementsType(
                            weight=freightcom_rest_req.WeightType(
                                unit="kg",
                                value=parcel.weight.KG
                            ),
                            cuboid=freightcom_rest_req.CuboidType(
                                unit="cm",
                                l=parcel.length.CM,
                                w=parcel.width.CM,
                                h=parcel.height.CM
                            )
                        ),
                        description=parcel.description or "N/A",
                    ) for parcel in packages
                ] if packaging_type == "package" else [],
                    courierpaks=[
                    freightcom_rest_req.CourierpakType(
                        measurements=freightcom_rest_req.CourierpakMeasurementsType(
                            weight=freightcom_rest_req.WeightType(
                                unit="kg",
                                value=parcel.weight.KG
                            ),
                        ),
                        description=parcel.description or "N/A",
                    ) for parcel in packages
                ] if packaging_type == "courier-pak" else [],
            ),
            reference_codes=[payload.reference] if payload.reference else []
        ),
        customs_invoice=(
            freightcom_rest_req.CustomsInvoiceType(
                source="details",
                broker=freightcom_rest_req.BrokerType(
                  use_carrier=True,
                ),
                details=freightcom_rest_req.CustomsInvoiceDetailsType(
                    products=[
                        freightcom_rest_req.ProductType(
                            product_name=item.description,
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
                            description=item.description
                        ) for item in customs.commodities
                    ],
                    tax_recipient=freightcom_rest_req.TaxRecipientType(
                        type=provider_units.PaymentType.map(
                                customs.duty.paid_by
                            ).value
                        or "shipper",
                        name=customs.duty_billing_address.company_name or customs.duty.person_name,
                        address=freightcom_rest_req.AddressType(
                            address_line_1=customs.duty_billing_address.address_line1,
                            address_line_2=customs.duty_billing_address.address_line2,
                            city=customs.duty_billing_address.city,
                            region=customs.duty_billing_address.state_code,
                            country=customs.duty_billing_address.country_code,
                            postal_code=customs.duty_billing_address.postal_code,
                        ),
                        phone_number=freightcom_rest_req.NumberType(
                            number=customs.duty_billing_address.phone_number
                        ),
                        reason_for_export=provider_units.CustomsContentType.map(
                            customs.content_type
                        ).value,
                    )
                )
            )
            if customs and customs.commodities
            else None
        ),
        #TODO: validate if we need to do pickup in the ship request
        # pickup_details=freightcom.PickupDetailsType(
        #
        # )
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(label_type=payload.label_type or "PDF")
    )
