import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ConsigneeAddressType:
    postalCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ConsignorAddressType:
    postalCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    dimensionUom: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    weight: typing.Optional[float] = None
    weightUom: typing.Optional[str] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class RateRequestType:
    consigneeAddress: typing.Optional[ConsigneeAddressType] = jstruct.JStruct[ConsigneeAddressType]
    consignorAddress: typing.Optional[ConsignorAddressType] = jstruct.JStruct[ConsignorAddressType]
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    productCode: typing.Optional[str] = None
    accountNumber: typing.Optional[str] = None