import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class NumberType:
    number: typing.Optional[str] = None
    extension: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BrokerType:
    use_carrier: typing.Optional[bool] = None
    name: typing.Optional[str] = None
    account_number: typing.Optional[str] = None
    phone_number: typing.Optional[NumberType] = jstruct.JStruct[NumberType]
    fax_number: typing.Optional[NumberType] = jstruct.JStruct[NumberType]
    email_address: typing.Optional[str] = None
    usmca_number: typing.Optional[str] = None
    fda_number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ProductCompositionAllocationType:
    provided: typing.Optional[bool] = None
    steel_percentage: typing.Optional[int] = None
    aluminum_percentage: typing.Optional[int] = None
    copper_percentage: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class TotalCostType:
    currency: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class WeightType:
    unit: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ProductType:
    product_name: typing.Optional[str] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    hs_code: typing.Optional[str] = None
    country_of_origin: typing.Optional[str] = None
    num_units: typing.Optional[int] = None
    unit_price: typing.Optional[TotalCostType] = jstruct.JStruct[TotalCostType]
    description: typing.Optional[str] = None
    cusma_included: typing.Optional[bool] = None
    non_auto_parts: typing.Optional[bool] = None
    fda_regulated: typing.Optional[str] = None
    product_composition_allocation: typing.Optional[ProductCompositionAllocationType] = jstruct.JStruct[ProductCompositionAllocationType]
    product_composition_allocation_zero: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class AddressType:
    address_line_1: typing.Optional[str] = None
    address_line_2: typing.Optional[str] = None
    unit_number: typing.Optional[str] = None
    city: typing.Optional[str] = None
    region: typing.Optional[str] = None
    country: typing.Optional[str] = None
    postal_code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TaxRecipientType:
    type: typing.Optional[str] = None
    shipper_tax_identifier: typing.Optional[str] = None
    receiver_tax_identifier: typing.Optional[str] = None
    third_party_tax_identifier: typing.Optional[str] = None
    other_tax_identifier: typing.Optional[str] = None
    name: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    phone_number: typing.Optional[NumberType] = jstruct.JStruct[NumberType]
    reason_for_export: typing.Optional[str] = None
    additional_remarks: typing.Optional[str] = None
    comments: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsInvoiceDetailsType:
    tax_recipient: typing.Optional[TaxRecipientType] = jstruct.JStruct[TaxRecipientType]
    products: typing.Optional[typing.List[ProductType]] = jstruct.JList[ProductType]


@attr.s(auto_attribs=True)
class CustomsInvoiceType:
    source: typing.Optional[str] = None
    broker: typing.Optional[BrokerType] = jstruct.JStruct[BrokerType]
    details: typing.Optional[CustomsInvoiceDetailsType] = jstruct.JStruct[CustomsInvoiceDetailsType]


@attr.s(auto_attribs=True)
class CustomsDataType:
    products: typing.Optional[typing.List[ProductType]] = jstruct.JList[ProductType]
    request_guaranteed_customs_charges: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ReadyType:
    hour: typing.Optional[int] = None
    minute: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DestinationType:
    name: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    residential: typing.Optional[bool] = None
    tailgate_required: typing.Optional[bool] = None
    instructions: typing.Optional[str] = None
    contact_name: typing.Optional[str] = None
    phone_number: typing.Optional[NumberType] = jstruct.JStruct[NumberType]
    email_addresses: typing.Optional[typing.List[str]] = None
    receives_email_updates: typing.Optional[bool] = None
    ready_at: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    ready_until: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    signature_requirement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DateType:
    year: typing.Optional[int] = None
    month: typing.Optional[int] = None
    day: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class InsuranceType:
    type: typing.Optional[str] = None
    total_cost: typing.Optional[TotalCostType] = jstruct.JStruct[TotalCostType]


@attr.s(auto_attribs=True)
class CourierpakMeasurementsType:
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]


@attr.s(auto_attribs=True)
class CourierpakType:
    measurements: typing.Optional[CourierpakMeasurementsType] = jstruct.JStruct[CourierpakMeasurementsType]
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DangerousGoodsDetailsType:
    packaging_group: typing.Optional[str] = None
    goods_class: typing.Optional[str] = None
    description: typing.Optional[str] = None
    united_nations_number: typing.Optional[str] = None
    emergency_contact_name: typing.Optional[str] = None
    emergency_contact_phone_number: typing.Optional[NumberType] = jstruct.JStruct[NumberType]


@attr.s(auto_attribs=True)
class CuboidType:
    unit: typing.Optional[str] = None
    l: typing.Optional[int] = None
    w: typing.Optional[int] = None
    h: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PackageMeasurementsType:
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    cuboid: typing.Optional[CuboidType] = jstruct.JStruct[CuboidType]


@attr.s(auto_attribs=True)
class PackageType:
    measurements: typing.Optional[PackageMeasurementsType] = jstruct.JStruct[PackageMeasurementsType]
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InBondDetailsType:
    type: typing.Optional[str] = None
    name: typing.Optional[str] = None
    address: typing.Optional[str] = None
    contact_method: typing.Optional[str] = None
    contact_email_address: typing.Optional[str] = None
    contact_phone_number: typing.Optional[NumberType] = jstruct.JStruct[NumberType]


@attr.s(auto_attribs=True)
class PalletServiceDetailsType:
    limited_access_delivery_type: typing.Optional[str] = None
    limited_access_delivery_other_name: typing.Optional[str] = None
    in_bond: typing.Optional[bool] = None
    in_bond_details: typing.Optional[InBondDetailsType] = jstruct.JStruct[InBondDetailsType]
    appointment_delivery: typing.Optional[bool] = None
    protect_from_freeze: typing.Optional[bool] = None
    threshold_pickup: typing.Optional[bool] = None
    threshold_delivery: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class PalletType:
    measurements: typing.Optional[PackageMeasurementsType] = jstruct.JStruct[PackageMeasurementsType]
    description: typing.Optional[str] = None
    freight_class: typing.Optional[str] = None
    nmfc: typing.Optional[str] = None
    contents_type: typing.Optional[str] = None
    num_pieces: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PackagingPropertiesType:
    pallet_type: typing.Optional[str] = None
    has_stackable_pallets: typing.Optional[bool] = None
    dangerous_goods: typing.Optional[str] = None
    dangerous_goods_details: typing.Optional[DangerousGoodsDetailsType] = jstruct.JStruct[DangerousGoodsDetailsType]
    pallets: typing.Optional[typing.List[PalletType]] = jstruct.JList[PalletType]
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    courierpaks: typing.Optional[typing.List[CourierpakType]] = jstruct.JList[CourierpakType]
    includes_return_label: typing.Optional[bool] = None
    special_handling_required: typing.Optional[bool] = None
    has_dangerous_goods: typing.Optional[bool] = None
    pallet_service_details: typing.Optional[PalletServiceDetailsType] = jstruct.JStruct[PalletServiceDetailsType]


@attr.s(auto_attribs=True)
class ShipmentRequestDetailsType:
    origin: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    expected_ship_date: typing.Optional[DateType] = jstruct.JStruct[DateType]
    packaging_type: typing.Optional[str] = None
    packaging_properties: typing.Optional[PackagingPropertiesType] = jstruct.JStruct[PackagingPropertiesType]
    insurance: typing.Optional[InsuranceType] = jstruct.JStruct[InsuranceType]
    reference_codes: typing.Optional[typing.List[str]] = None
    customs_data: typing.Optional[CustomsDataType] = jstruct.JStruct[CustomsDataType]


@attr.s(auto_attribs=True)
class DispatchDetailsType:
    date: typing.Optional[DateType] = jstruct.JStruct[DateType]
    ready_at: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    ready_until: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]


@attr.s(auto_attribs=True)
class PaperlessCustomsDocumentType:
    type: typing.Optional[str] = None
    type_other_name: typing.Optional[str] = None
    file_name: typing.Optional[str] = None
    file_base64: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupDetailsType:
    pre_scheduled_pickup: typing.Optional[bool] = None
    date: typing.Optional[DateType] = jstruct.JStruct[DateType]
    ready_at: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    ready_until: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    pickup_location: typing.Optional[str] = None
    contact_name: typing.Optional[str] = None
    contact_phone_number: typing.Optional[NumberType] = jstruct.JStruct[NumberType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    unique_id: typing.Optional[str] = None
    payment_method_id: typing.Optional[str] = None
    customs_and_duties_payment_method_id: typing.Optional[str] = None
    service_id: typing.Optional[str] = None
    details: typing.Optional[ShipmentRequestDetailsType] = jstruct.JStruct[ShipmentRequestDetailsType]
    customs_invoice: typing.Optional[CustomsInvoiceType] = jstruct.JStruct[CustomsInvoiceType]
    pickup_details: typing.Optional[PickupDetailsType] = jstruct.JStruct[PickupDetailsType]
    dispatch_details: typing.Optional[DispatchDetailsType] = jstruct.JStruct[DispatchDetailsType]
    paperless_customs_documents: typing.Optional[typing.List[PaperlessCustomsDocumentType]] = jstruct.JList[PaperlessCustomsDocumentType]
