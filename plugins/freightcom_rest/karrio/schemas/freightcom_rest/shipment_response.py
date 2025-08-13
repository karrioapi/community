import attr
import jstruct
import typing


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
class PhoneNumberType:
    number: typing.Optional[str] = None
    extension: typing.Optional[int] = None


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
    phone_number: typing.Optional[PhoneNumberType] = jstruct.JStruct[PhoneNumberType]
    email_addresses: typing.Optional[typing.List[str]] = None
    receives_email_updates: typing.Optional[bool] = None
    ready_at: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    ready_until: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    signature_requirement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExpectedShipDateType:
    year: typing.Optional[int] = None
    month: typing.Optional[int] = None
    day: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BaseType:
    currency: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class InsuranceType:
    type: typing.Optional[str] = None
    total_cost: typing.Optional[BaseType] = jstruct.JStruct[BaseType]


@attr.s(auto_attribs=True)
class WeightType:
    unit: typing.Optional[str] = None
    value: typing.Optional[float] = None


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
    emergency_contact_phone_number: typing.Optional[PhoneNumberType] = jstruct.JStruct[PhoneNumberType]


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
    contact_phone_number: typing.Optional[PhoneNumberType] = jstruct.JStruct[PhoneNumberType]


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
class DetailsType:
    origin: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    expected_ship_date: typing.Optional[ExpectedShipDateType] = jstruct.JStruct[ExpectedShipDateType]
    packaging_type: typing.Optional[str] = None
    packaging_properties: typing.Optional[PackagingPropertiesType] = jstruct.JStruct[PackagingPropertiesType]
    insurance: typing.Optional[InsuranceType] = jstruct.JStruct[InsuranceType]
    reference_codes: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class LabelType:
    size: typing.Optional[str] = None
    format: typing.Optional[str] = None
    url: typing.Optional[str] = None
    padded: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class SurchargeType:
    type: typing.Optional[str] = None
    amount: typing.Optional[BaseType] = jstruct.JStruct[BaseType]


@attr.s(auto_attribs=True)
class RateType:
    carrier_name: typing.Optional[str] = None
    service_name: typing.Optional[str] = None
    service_id: typing.Optional[str] = None
    valid_until: typing.Optional[ExpectedShipDateType] = jstruct.JStruct[ExpectedShipDateType]
    total: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    base: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    surcharges: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    taxes: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    transit_time_days: typing.Optional[int] = None
    transit_time_not_available: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class TransportDataType:
    pass


@attr.s(auto_attribs=True)
class ShipmentType:
    id: typing.Optional[str] = None
    unique_id: typing.Optional[str] = None
    state: typing.Optional[str] = None
    transaction_number: typing.Optional[str] = None
    primary_tracking_number: typing.Optional[str] = None
    tracking_numbers: typing.Optional[typing.List[str]] = None
    tracking_url: typing.Optional[str] = None
    return_tracking_number: typing.Optional[str] = None
    bol_number: typing.Optional[str] = None
    pickup_confirmation_number: typing.Optional[str] = None
    details: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    transport_data: typing.Optional[TransportDataType] = jstruct.JStruct[TransportDataType]
    labels: typing.Optional[typing.List[LabelType]] = jstruct.JList[LabelType]
    customs_invoice_url: typing.Optional[str] = None
    rate: typing.Optional[RateType] = jstruct.JStruct[RateType]
    order_source: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
