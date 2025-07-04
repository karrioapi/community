"""SendCloud shipment response schema."""

import attr
from typing import Optional, List, Dict, Any


@attr.s(auto_attribs=True)
class ShipmentInfoType:
    id: Optional[int] = None
    name: Optional[str] = None


@attr.s(auto_attribs=True)
class LabelType:
    normal_printer: Optional[List[Any]] = None
    label_printer: Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsDeclarationType:
    id: Optional[int] = None
    currency: Optional[str] = None
    content: Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelItemResponseType:
    description: Optional[str] = None
    quantity: Optional[int] = None
    weight: Optional[str] = None
    value: Optional[str] = None
    sku: Optional[str] = None
    hs_code: Optional[str] = None
    origin_country: Optional[str] = None


@attr.s(auto_attribs=True)
class StatusType:
    id: Optional[int] = None
    message: Optional[str] = None


@attr.s(auto_attribs=True)
class CarrierType:
    code: Optional[str] = None
    name: Optional[str] = None


@attr.s(auto_attribs=True)
class DocumentType:
    type: Optional[str] = None
    size: Optional[str] = None
    link: Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    id: Optional[int] = None
    name: Optional[str] = None
    company_name: Optional[str] = None
    address: Optional[str] = None
    address_2: Optional[str] = None
    house_number: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    date_created: Optional[str] = None
    date_updated: Optional[str] = None
    shipment: Optional[ShipmentInfoType] = None
    weight: Optional[str] = None
    height: Optional[str] = None
    length: Optional[str] = None
    width: Optional[str] = None
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    label: Optional[LabelType] = None
    customs_declaration: Optional[CustomsDeclarationType] = None
    parcel_items: Optional[List[ParcelItemResponseType]] = None
    status: Optional[StatusType] = None
    carrier: Optional[CarrierType] = None
    external_order_id: Optional[str] = None
    external_shipment_id: Optional[str] = None
    total_order_value: Optional[str] = None
    total_order_value_currency: Optional[str] = None
    is_return: Optional[bool] = None
    insured_value: Optional[int] = None
    to_service_point: Optional[int] = None
    documents: Optional[List[DocumentType]] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    parcel: Optional[ParcelType] = None 
