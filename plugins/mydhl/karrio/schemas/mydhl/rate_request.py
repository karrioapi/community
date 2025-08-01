import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipperDetailsType:
    postalCode: typing.Optional[str] = None
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverDetailsType:
    postalCode: typing.Optional[str] = None
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[ShipperDetailsType] = None
    receiverDetails: typing.Optional[ReceiverDetailsType] = None


@attr.s(auto_attribs=True)
class AccountType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class PackageType:
    weight: typing.Optional[float] = None
    dimensions: typing.Optional[DimensionsType] = None


@attr.s(auto_attribs=True)
class RateRequestType:
    customerDetails: typing.Optional[CustomerDetailsType] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
