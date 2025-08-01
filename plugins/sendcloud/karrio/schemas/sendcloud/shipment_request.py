import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ParcelItemType:
    description: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    weight: typing.Optional[str] = None
    value: typing.Optional[str] = None
    hs_code: typing.Optional[str] = None
    origin_country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsDeclarationType:
    contents: typing.Optional[str] = None
    invoice_nr: typing.Optional[str] = None
    non_delivery: typing.Optional[str] = None
    shipment_type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    name: typing.Optional[str] = None
    company_name: typing.Optional[str] = None
    address: typing.Optional[str] = None
    address_2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    postal_code: typing.Optional[str] = None
    country: typing.Optional[str] = None
    telephone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    weight: typing.Optional[str] = None
    order_number: typing.Optional[str] = None
    service_point_id: typing.Optional[str] = None
    require_signature: typing.Optional[bool] = None
    insured_value: typing.Optional[float] = None
    reference: typing.Optional[str] = None
    shipping_method: typing.Optional[str] = None
    parcel_items: typing.Optional[typing.List[ParcelItemType]] = jstruct.JList[ParcelItemType]
    customs_declaration: typing.Optional[CustomsDeclarationType] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    parcel: typing.Optional[ParcelType] = None
