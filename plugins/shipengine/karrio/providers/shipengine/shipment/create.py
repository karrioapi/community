"""Karrio ShipEngine shipment API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract shipment details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., ShipmentRequestType),
# while XML schema types don't have this suffix (e.g., ShipmentRequest).

import karrio.schemas.shipengine.shipment_request as shipengine_req
import karrio.schemas.shipengine.shipment_response as shipengine_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils
import karrio.providers.shipengine.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if we have valid shipment data
    
    has_shipment = response.xpath(".//shipment") if hasattr(response, 'xpath') else False
    

    shipment = _extract_details(response, settings) if has_shipment else None

    return shipment, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """
    Extract shipment details from carrier response data

    data: The carrier-specific shipment data structure
    settings: The carrier connection settings

    Returns a ShipmentDetails object with extracted shipment information
    """
    # Convert the carrier data to a proper object for easy attribute access
    
    # For XML APIs, convert Element to proper response object
    shipment = lib.to_object(shipengine_res.ShipmentResponse, data)

    # Extract tracking info
    tracking_number = shipment.tracking_number if hasattr(shipment, 'tracking_number') else ""
    shipment_id = shipment.shipment_id if hasattr(shipment, 'shipment_id') else ""

    # Extract label info
    label_format = shipment.label_format if hasattr(shipment, 'label_format') else "PDF"
    label_base64 = shipment.label_image if hasattr(shipment, 'label_image') else ""

    # Extract optional invoice
    invoice_base64 = shipment.invoice_image if hasattr(shipment, 'invoice_image') else ""

    # Extract service code for metadata
    service_code = shipment.service_code if hasattr(shipment, 'service_code') else ""
    

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
            service_code=service_code,
            # Add any other relevant metadata from the carrier's response
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
    
    # For XML API request
    request = shipengine_req.ShipmentRequest(
        # Map shipper details
        shipper=shipengine_req.Address(
            address_line1=shipper.address_line1,
            city=shipper.city,
            postal_code=shipper.postal_code,
            country_code=shipper.country_code,
            state_code=shipper.state_code,
            person_name=shipper.person_name,
            company_name=shipper.company_name,
            phone_number=shipper.phone_number,
            email=shipper.email,
        ),
        # Map recipient details
        recipient=shipengine_req.Address(
            address_line1=recipient.address_line1,
            city=recipient.city,
            postal_code=recipient.postal_code,
            country_code=recipient.country_code,
            state_code=recipient.state_code,
            person_name=recipient.person_name,
            company_name=recipient.company_name,
            phone_number=recipient.phone_number,
            email=recipient.email,
        ),
        # Map package details
        packages=[
            shipengine_req.Package(
                weight=package.weight.value,
                weight_unit=provider_units.WeightUnit[package.weight.unit].value,
                length=package.length.value if package.length else None,
                width=package.width.value if package.width else None,
                height=package.height.value if package.height else None,
                dimension_unit=provider_units.DimensionUnit[package.dimension_unit].value if package.dimension_unit else None,
                packaging_type=provider_units.PackagingType[package.packaging_type or 'your_packaging'].value,
            )
            for package in packages
        ],
        # Add service code
        service_code=service,
        # Add account information
        customer_number=settings.customer_number,
        # Add label details
        label_format=payload.label_type or "PDF",
        # Add any other required fields for the carrier API
    )
    

    return lib.Serializable(request, lib.to_xml)
