"""SendCloud shipment request schema."""

import attr
from typing import Optional, List


@attr.s(auto_attribs=True)
class ShipmentType:
    id: Optional[int] = None
    name: Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelItemType:
    description: Optional[str] = None
    quantity: Optional[int] = None
    weight: Optional[str] = None
    value: Optional[str] = None
    sku: Optional[str] = None
    hs_code: Optional[str] = None
    origin_country: Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelRequestType:
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
    shipment: Optional[ShipmentType] = None
    weight: Optional[str] = None
    height: Optional[str] = None
    length: Optional[str] = None
    width: Optional[str] = None
    parcel_items: Optional[List[ParcelItemType]] = None
    customs_invoice_nr: Optional[str] = None
    customs_shipment_type: Optional[str] = None
    external_order_id: Optional[str] = None
    external_shipment_id: Optional[str] = None
    total_order_value: Optional[str] = None
    total_order_value_currency: Optional[str] = None
    is_return: Optional[bool] = None
    insured_value: Optional[int] = None
    to_service_point: Optional[int] = None
    request_label: Optional[bool] = None
    request_label_async: Optional[bool] = None
    apply_shipping_rules: Optional[bool] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    parcel: Optional[ParcelRequestType] = None 
