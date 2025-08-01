import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentHeaderType:
    messageType: typing.Optional[str] = None
    messageDateTime: typing.Optional[str] = None
    messageVersion: typing.Optional[str] = None
    accessToken: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentConsigneeAddressType:
    name: typing.Optional[str] = None
    address1: typing.Optional[str] = None
    address2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentConsignorAddressType:
    name: typing.Optional[str] = None
    address1: typing.Optional[str] = None
    address2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentDimensionsType:
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    dimensionUom: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentPackageType:
    weight: typing.Optional[float] = None
    weightUom: typing.Optional[str] = None
    dimensions: typing.Optional[ShipmentDimensionsType] = jstruct.JStruct[ShipmentDimensionsType]
    packageId: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentBodyType:
    consigneeAddress: typing.Optional[ShipmentConsigneeAddressType] = jstruct.JStruct[ShipmentConsigneeAddressType]
    consignorAddress: typing.Optional[ShipmentConsignorAddressType] = jstruct.JStruct[ShipmentConsignorAddressType]
    packages: typing.Optional[typing.List[ShipmentPackageType]] = jstruct.JList[ShipmentPackageType]
    productCode: typing.Optional[str] = None
    accountNumber: typing.Optional[str] = None
    pickupId: typing.Optional[str] = None
    distributionCenter: typing.Optional[str] = None
    labelFormat: typing.Optional[str] = None
    labelSize: typing.Optional[str] = None
    orderedProductId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    header: typing.Optional[ShipmentHeaderType] = jstruct.JStruct[ShipmentHeaderType]
    body: typing.Optional[ShipmentBodyType] = jstruct.JStruct[ShipmentBodyType]
