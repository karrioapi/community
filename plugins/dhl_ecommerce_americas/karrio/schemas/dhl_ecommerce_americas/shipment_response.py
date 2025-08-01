import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentResponseHeaderType:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None
    messageDetail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageResultType:
    packageId: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    orderedProductId: typing.Optional[str] = None
    labelImage: typing.Optional[str] = None
    labelFormat: typing.Optional[str] = None
    labelSize: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseBodyType:
    packageResults: typing.Optional[typing.List[PackageResultType]] = jstruct.JList[PackageResultType]


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    header: typing.Optional[ShipmentResponseHeaderType] = jstruct.JStruct[ShipmentResponseHeaderType]
    body: typing.Optional[ShipmentResponseBodyType] = jstruct.JStruct[ShipmentResponseBodyType]