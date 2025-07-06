import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class RateOptionsType:
    calculate_tax_amount: typing.Optional[bool] = None
    preferred_currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    unit: typing.Optional[str] = None
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class WeightType:
    value: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    package_code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipType:
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company_name: typing.Optional[str] = None
    address_line1: typing.Optional[str] = None
    address_line2: typing.Optional[str] = None
    address_line3: typing.Optional[str] = None
    city_locality: typing.Optional[str] = None
    state_province: typing.Optional[str] = None
    postal_code: typing.Optional[int] = None
    country_code: typing.Optional[str] = None
    address_residential_indicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    validate_address: typing.Optional[str] = None
    ship_to: typing.Optional[ShipType] = jstruct.JStruct[ShipType]
    ship_from: typing.Optional[ShipType] = jstruct.JStruct[ShipType]
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]


@attr.s(auto_attribs=True)
class RateRequestType:
    rate_options: typing.Optional[RateOptionsType] = jstruct.JStruct[RateOptionsType]
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
