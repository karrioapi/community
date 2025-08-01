"""Karrio DHL eCommerce Americas shipment creation implementation."""

import typing
import datetime
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_americas.error as error
import karrio.providers.dhl_ecommerce_americas.utils as provider_utils
import karrio.providers.dhl_ecommerce_americas.units as provider_units
import karrio.schemas.dhl_ecommerce_americas.shipment_request as dhl_req
import karrio.schemas.dhl_ecommerce_americas.shipment_response as dhl_res

def parse_shipment_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Convert to typed object using generated schema
    shipment_response = lib.to_object(dhl_res.ShipmentResponseType, response)
    
    shipment = None
    if (shipment_response.body and 
        shipment_response.body.packageResults and 
        len(shipment_response.body.packageResults) > 0):
        
        package_result = shipment_response.body.packageResults[0]
        shipment = _extract_details(lib.to_dict(package_result), settings)

    return shipment, messages

def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from DHL response data"""

    # Convert the DHL data to a proper object for easy attribute access
    package_result = lib.to_object(dhl_res.PackageResultType, data)
    
    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=package_result.trackingNumber,
        shipment_identifier=package_result.packageId,
        docs=models.Documents(
            label=package_result.labelImage if hasattr(package_result, 'labelImage') else None,
        ),
        meta=dict(
            package_id=package_result.packageId if hasattr(package_result, 'packageId') else "",
            ordered_product_id=package_result.orderedProductId if hasattr(package_result, 'orderedProductId') else "",
            label_format=package_result.labelFormat if hasattr(package_result, 'labelFormat') else "PNG",
            label_size=package_result.labelSize if hasattr(package_result, 'labelSize') else "4x6",
            service_name="DHL eCommerce Americas",
        ),
    )

def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for the DHL eCommerce Americas API"""

    # Convert karrio models to DHL-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    service_code = payload.service or provider_units.ShippingService.dhl_parcel_ground.value
    message_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # Create the DHL-specific request object using generated types
    request = dhl_req.ShipmentRequestType(
        header=dhl_req.ShipmentHeaderType(
            messageType="LABEL",
            messageDateTime=message_datetime,
            messageVersion="1.0",
            accessToken="",  # Will be set by proxy
        ),
        body=dhl_req.ShipmentBodyType(
            consigneeAddress=dhl_req.ShipmentConsigneeAddressType(
                name=recipient.person_name or recipient.company_name or "Recipient",
                address1=recipient.address_line,
                address2=recipient.address_line2 or "",
                city=recipient.city,
                state=recipient.state_code,
                postalCode=recipient.postal_code,
                countryCode=recipient.country_code,
                phoneNumber=recipient.phone_number or "",
                email=recipient.email or "",
            ),
            consignorAddress=dhl_req.ShipmentConsignorAddressType(
                name=shipper.person_name or shipper.company_name or "Shipper",
                address1=shipper.address_line,
                address2=shipper.address_line2 or "",
                city=shipper.city,
                state=shipper.state_code,
                postalCode=shipper.postal_code,
                countryCode=shipper.country_code,
                phoneNumber=shipper.phone_number or "",
                email=shipper.email or "",
            ),
            packages=[
                dhl_req.ShipmentPackageType(
                    weight=package.weight.LB,
                    weightUom="LB",
                    dimensions=dhl_req.ShipmentDimensionsType(
                        length=package.length.IN if package.length else None,
                        width=package.width.IN if package.width else None,
                        height=package.height.IN if package.height else None,
                        dimensionUom="IN",
                    ) if all([package.length, package.width, package.height]) else None,
                    packageId=f"PKG_{index + 1}",
                    description=package.items.description if package.items else "Package",
                )
                for index, package in enumerate(packages)
            ],
            productCode=service_code,
            accountNumber=getattr(settings, 'account_number', ''),
            pickupId=getattr(settings, 'pickup_id', ''),
            distributionCenter=getattr(settings, 'distribution_center', ''),
            labelFormat="PNG",
            labelSize="4x6",
            orderedProductId=payload.reference or f"ORDER_{lib.uuid()}",
        )
    )

    return lib.Serializable(request, lib.to_dict)