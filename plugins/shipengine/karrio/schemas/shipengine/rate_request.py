import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Address:
    address_line1: str
    city_locality: str
    postal_code: str
    country_code: str
    state_province: typing.Optional[str] = None
    address_line2: typing.Optional[str] = None
    address_line3: typing.Optional[str] = None
    name: typing.Optional[str] = None
    company_name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Weight:
    value: float
    unit: str = "pound"


@attr.s(auto_attribs=True)
class Dimensions:
    length: float
    width: float
    height: float
    unit: str = "inch"


@attr.s(auto_attribs=True)
class Package:
    weight: Weight
    dimensions: typing.Optional[Dimensions] = None
    package_code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateRequest:
    ship_from: Address
    ship_to: Address
    packages: typing.List[Package]
    rate_options: typing.Optional[typing.Dict[str, typing.Any]] = None
    shipment_id: typing.Optional[str] = None
    carrier_ids: typing.Optional[typing.List[str]] = None
    service_codes: typing.Optional[typing.List[str]] = None
    package_types: typing.Optional[typing.List[str]] = None
    calculate_tax_amount: typing.Optional[bool] = None
    compare_delivery_dates: typing.Optional[bool] = None
    tags: typing.Optional[typing.List[str]] = None
    shipment_date: typing.Optional[str] = None
    confirmation: typing.Optional[str] = None
    comparison_rate_type: typing.Optional[str] = None
    insurance_amount: typing.Optional[typing.Dict[str, typing.Any]] = None 
