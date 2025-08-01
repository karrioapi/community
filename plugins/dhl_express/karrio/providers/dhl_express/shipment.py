from typing import Tuple, List
import datetime
from karrio.core.utils import Serializable, Deserializable, DF, SF
from karrio.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message,
    Documents,
)
from karrio.providers.dhl_express.utils import Settings, request
from karrio.providers.dhl_express.error import parse_error_response
import karrio.providers.dhl_express.units as provider_units
import karrio.lib as lib


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[ShipmentDetails, List[Message]]:
    response = _response.deserialize()
    messages: List[Message] = parse_error_response(response, settings)
    shipment = _extract_shipment_details(response, settings) if "shipmentTrackingNumber" in response else None

    return shipment, messages


def _extract_shipment_details(data: dict, settings: Settings) -> ShipmentDetails:
    documents = data.get("documents", [])
    label_content = documents[0].get("content") if documents else None
    
    return ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=data.get("shipmentTrackingNumber"),
        shipment_identifier=data.get("shipmentTrackingNumber"),
        docs=Documents(
            label=label_content
        ) if label_content else None,
        meta=data,
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable:
    """Create shipment request for DHL Express."""
    
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    
    packages = lib.to_packages(payload.parcels)
    package = packages[0]
    
    request_data = {
        "plannedShippingDateAndTime": lib.fdatetime(
            options.shipment_date.state or datetime.datetime.now(),
            output_format="%Y-%m-%dT%H:%M:%S"
        ),
        "pickup": {
            "isRequested": True,
            "pickupDetails": {
                "postalAddress": {
                    "postalCode": payload.shipper.postal_code,
                    "cityName": payload.shipper.city,
                    "countryCode": payload.shipper.country_code,
                    "addressLine1": payload.shipper.address_line1 or "",
                }
            }
        },
        "productCode": getattr(payload, "service", "EXPRESS_WORLDWIDE"),
        "accounts": [
            {
                "typeCode": "shipper",
                "number": settings.account_number
            }
        ] if settings.account_number else [],
        "customerDetails": {
            "shipperDetails": {
                "postalAddress": {
                    "postalCode": payload.shipper.postal_code,
                    "cityName": payload.shipper.city,
                    "countryCode": payload.shipper.country_code,
                    "addressLine1": payload.shipper.address_line1 or "",
                },
                "contactInformation": {
                    "email": payload.shipper.email or "",
                    "phone": payload.shipper.phone_number or "",
                    "companyName": payload.shipper.company_name or "",
                    "fullName": payload.shipper.person_name or "",
                }
            },
            "receiverDetails": {
                "postalAddress": {
                    "postalCode": payload.recipient.postal_code,
                    "cityName": payload.recipient.city,
                    "countryCode": payload.recipient.country_code,
                    "addressLine1": payload.recipient.address_line1 or "",
                },
                "contactInformation": {
                    "email": payload.recipient.email or "",
                    "phone": payload.recipient.phone_number or "",
                    "companyName": payload.recipient.company_name or "",
                    "fullName": payload.recipient.person_name or "",
                }
            }
        },
        "packages": [
            {
                "weight": package.weight.value,
                "dimensions": {
                    "length": package.length.value,
                    "width": package.width.value,
                    "height": package.height.value,
                },
            }
            for package in packages
        ],
        "content": {
            "packages": [
                {
                    "weight": package.weight.value,
                    "customerReferences": [
                        {
                            "value": payload.reference or "",
                            "typeCode": "CU"
                        }
                    ],
                }
                for package in packages
            ],
            "isCustomsDeclarable": payload.customs is not None,
            "description": (payload.customs.content_description if payload.customs else "Documents"),
            "invoice": {
                "number": payload.reference or "",
                "date": lib.fdate(),
                "function": "commercial",
            } if payload.customs else None,
        },
        "outputImageProperties": {
            "printerDPI": 300,
            "customerLogos": [],
            "customerBarcode": "",
            "splitTransportAndWaybillDocLabels": False,
            "allDocumentsInOneImage": False,
            "splitDocumentsByPages": False,
            "splitInvoiceAndReceipt": False,
            "receiptAndLabelsInOneImage": False,
        },
    }
    
    return Serializable(request_data, lib.to_dict)


def create_shipment(payload: ShipmentRequest, settings: Settings) -> Deserializable[str]:
    """Create shipment with DHL Express."""
    
    request_data = shipment_request(payload, settings)
    response = request(
        url=f"{settings.server_url}/shipments",
        data=request_data.serialize(),
        trace=payload.reference,
        method="POST",
        settings=settings,
    )
    
    return Deserializable(response, lib.to_dict)


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[ConfirmationDetails, List[Message]]:
    response = _response.deserialize()
    messages: List[Message] = parse_error_response(response, settings)
    success = response.get("cancelled", False) or len(messages) == 0
    confirmation: ConfirmationDetails = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        operation="Cancel Shipment",
        success=success,
    )

    return confirmation, messages


def shipment_cancel_request(payload: ShipmentCancelRequest, settings: Settings) -> Serializable:
    """Create shipment cancel request for DHL Express."""
    
    request_data = {
        "shipmentTrackingNumber": payload.shipment_identifier,
        "reason": "001",  # Default reason code
    }

    return Serializable(request_data, lib.to_dict)


def cancel_shipment(payload: ShipmentCancelRequest, settings: Settings) -> Deserializable[str]:
    """Cancel shipment with DHL Express."""
    
    request_data = shipment_cancel_request(payload, settings)
    response = request(
        url=f"{settings.server_url}/shipments/{payload.shipment_identifier}",
        data=request_data.serialize(),
        trace=payload.shipment_identifier,
        method="DELETE",
        settings=settings,
    )
    
    return Deserializable(response, lib.to_dict)
