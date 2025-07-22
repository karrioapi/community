import datetime
import karrio.schemas.dhl_ecommerce_americas.shipment_response as shipping
import typing
import base64
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_americas.error as error
import karrio.providers.dhl_ecommerce_americas.utils as provider_utils
import karrio.providers.dhl_ecommerce_americas.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    shipment = None
    if isinstance(response, dict):
        if "body" in response and "packageResults" in response["body"]:
            package_results = response["body"]["packageResults"]
            if package_results:
                shipment = _extract_details(package_results[0], settings)
        elif "packageResults" in response:
            package_results = response["packageResults"]
            if package_results:
                shipment = _extract_details(package_results[0], settings)

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    package_result = lib.to_object(shipping.PackageResult, data)
    
    # Decode label image if it's base64 encoded
    label_data = package_result.labelImage or ""
    
    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=package_result.trackingNumber,
        shipment_identifier=package_result.packageId,
        docs=models.Documents(
            label=label_data,
        ),
        meta=dict(
            package_id=package_result.packageId,
            ordered_product_id=package_result.orderedProductId,
            label_format=package_result.labelFormat,
            label_size=package_result.labelSize,
            service_name="DHL eCommerce Americas",
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
    
    service_code = payload.service or provider_units.ShippingService.dhl_parcel_ground.value
    
    # Get current datetime for message header
    message_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    request = {
        "header": {
            "messageType": "LABEL",
            "messageDateTime": message_datetime,
            "messageVersion": "1.0",
            "accessToken": "",  # Will be set by proxy
        },
        "body": {
            "consigneeAddress": {
                "name": recipient.person_name or recipient.company_name or "Recipient",
                "address1": recipient.address_line,
                "address2": recipient.address_line2 or "",
                "city": recipient.city,
                "state": recipient.state_code,
                "postalCode": recipient.postal_code,
                "countryCode": recipient.country_code,
                "phoneNumber": recipient.phone_number or "",
                "email": recipient.email or "",
            },
            "consignorAddress": {
                "name": shipper.person_name or shipper.company_name or "Shipper",
                "address1": shipper.address_line,
                "address2": shipper.address_line2 or "",
                "city": shipper.city,
                "state": shipper.state_code,
                "postalCode": shipper.postal_code,
                "countryCode": shipper.country_code,
                "phoneNumber": shipper.phone_number or "",
                "email": shipper.email or "",
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
                    "packageId": f"PKG_{index + 1}",
                    "description": package.items.description if package.items else "Package",
                }
                for index, package in enumerate(packages)
            ],
            "productCode": service_code,
            "accountNumber": getattr(settings, 'account_number', ''),
            "pickupId": getattr(settings, 'pickup_id', ''),
            "distributionCenter": getattr(settings, 'distribution_center', ''),
            "labelFormat": "PNG",
            "labelSize": "4x6",
            "orderedProductId": payload.reference or f"ORDER_{lib.uuid()}",
        }
    }

    return lib.Serializable(request, lib.to_dict)
