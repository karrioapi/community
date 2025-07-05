import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Address:
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company_name: typing.Optional[str] = None
    address_line1: str = None
    address_line2: typing.Optional[str] = None
    address_line3: typing.Optional[str] = None
    city_locality: str = None
    state_province: typing.Optional[str] = None
    postal_code: str = None
    country_code: str = None
    address_residential_indicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Weight:
    value: float
    unit: str


@attr.s(auto_attribs=True)
class Dimensions:
    unit: str
    length: float
    width: float
    height: float


@attr.s(auto_attribs=True)
class InsuredValue:
    currency: str
    amount: float


@attr.s(auto_attribs=True)
class Package:
    package_code: typing.Optional[str] = None
    weight: Weight = None
    dimensions: typing.Optional[Dimensions] = None
    insured_value: typing.Optional[InsuredValue] = None
    tracking_number: typing.Optional[str] = None
    reference1: typing.Optional[str] = None
    reference2: typing.Optional[str] = None
    reference3: typing.Optional[str] = None
    external_package_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsItem:
    description: str
    quantity: int
    value: InsuredValue
    harmonized_tariff_code: typing.Optional[str] = None
    country_of_origin: typing.Optional[str] = None
    unit_of_measure: typing.Optional[str] = None
    sku: typing.Optional[str] = None
    sku_description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsDeclaration:
    contents: str
    customs_items: typing.List[CustomsItem] = jstruct.JList[CustomsItem]
    non_delivery: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdvancedOptions:
    bill_to_account: typing.Optional[str] = None
    bill_to_country_code: typing.Optional[str] = None
    bill_to_party: typing.Optional[str] = None
    bill_to_postal_code: typing.Optional[str] = None
    contains_alcohol: typing.Optional[bool] = None
    delivered_duty_paid: typing.Optional[bool] = None
    non_machinable: typing.Optional[bool] = None
    saturday_delivery: typing.Optional[bool] = None
    use_ups_ground_freight_pricing: typing.Optional[bool] = None
    freight_class: typing.Optional[str] = None
    custom_field1: typing.Optional[str] = None
    custom_field2: typing.Optional[str] = None
    custom_field3: typing.Optional[str] = None
    origin_type: typing.Optional[str] = None
    shipper_release: typing.Optional[bool] = None
    collect_on_delivery: typing.Optional[InsuredValue] = None


@attr.s(auto_attribs=True)
class ShipmentRequest:
    validate_address: typing.Optional[str] = None
    carrier_id: typing.Optional[str] = None
    service_code: typing.Optional[str] = None
    external_order_id: typing.Optional[str] = None
    items: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None
    tax_identifiers: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None
    external_shipment_id: typing.Optional[str] = None
    ship_date: typing.Optional[str] = None
    ship_to: Address = None
    ship_from: Address = None
    warehouse_id: typing.Optional[str] = None
    return_to: typing.Optional[Address] = None
    confirmation: typing.Optional[str] = None
    customs: typing.Optional[CustomsDeclaration] = None
    advanced_options: typing.Optional[AdvancedOptions] = None
    insurance_provider: typing.Optional[str] = None
    tags: typing.Optional[typing.List[str]] = None
    packages: typing.List[Package] = jstruct.JList[Package]
    total_weight: typing.Optional[Weight] = None
    items: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None 
