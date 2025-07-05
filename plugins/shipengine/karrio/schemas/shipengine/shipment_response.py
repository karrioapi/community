import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Label:
    label_id: str
    status: str
    shipment_id: str
    ship_date: str
    created_at: str
    shipment_cost: typing.Dict[str, typing.Any]
    insurance_cost: typing.Dict[str, typing.Any]
    tracking_number: typing.Optional[str] = None
    is_return_label: typing.Optional[bool] = None
    rma_number: typing.Optional[str] = None
    is_international: typing.Optional[bool] = None
    batch_id: typing.Optional[str] = None
    carrier_id: typing.Optional[str] = None
    service_code: typing.Optional[str] = None
    package_code: typing.Optional[str] = None
    voided: typing.Optional[bool] = None
    voided_at: typing.Optional[str] = None
    label_format: typing.Optional[str] = None
    label_layout: typing.Optional[str] = None
    trackable: typing.Optional[bool] = None
    label_image_id: typing.Optional[str] = None
    carrier_code: typing.Optional[str] = None
    tracking_status: typing.Optional[str] = None
    label_download: typing.Optional[typing.Dict[str, typing.Any]] = None
    form_download: typing.Optional[typing.Dict[str, typing.Any]] = None
    insurance_claim: typing.Optional[typing.Dict[str, typing.Any]] = None
    packages: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None


@attr.s(auto_attribs=True)
class ShipmentResponse:
    shipment_id: str
    carrier_id: str
    service_code: str
    external_order_id: typing.Optional[str] = None
    items: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None
    tax_identifiers: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None
    external_shipment_id: typing.Optional[str] = None
    ship_date: typing.Optional[str] = None
    created_at: typing.Optional[str] = None
    modified_at: typing.Optional[str] = None
    shipment_status: typing.Optional[str] = None
    ship_to: typing.Optional[typing.Dict[str, typing.Any]] = None
    ship_from: typing.Optional[typing.Dict[str, typing.Any]] = None
    warehouse_id: typing.Optional[str] = None
    return_to: typing.Optional[typing.Dict[str, typing.Any]] = None
    confirmation: typing.Optional[str] = None
    customs: typing.Optional[typing.Dict[str, typing.Any]] = None
    advanced_options: typing.Optional[typing.Dict[str, typing.Any]] = None
    insurance_provider: typing.Optional[str] = None
    tags: typing.Optional[typing.List[str]] = None
    packages: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None
    total_weight: typing.Optional[typing.Dict[str, typing.Any]] = None
    labels: typing.Optional[typing.List[Label]] = jstruct.JList[Label] 
