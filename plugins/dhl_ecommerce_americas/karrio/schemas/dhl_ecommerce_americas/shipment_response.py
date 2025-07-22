import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PackageResult:
    packageId: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    labelImage: typing.Optional[str] = None
    labelFormat: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentBody:
    orderedProductId: typing.Optional[str] = None
    packageResults: typing.Optional[typing.List[PackageResult]] = jstruct.JList[PackageResult]


@attr.s(auto_attribs=True)
class ShipmentHeader:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponse:
    header: typing.Optional[ShipmentHeader] = jstruct.JStruct[ShipmentHeader]
    body: typing.Optional[ShipmentBody] = jstruct.JStruct[ShipmentBody]


@attr.s(auto_attribs=True)
class CancelResponse:
    header: typing.Optional[ShipmentHeader] = jstruct.JStruct[ShipmentHeader]
    body: typing.Optional[dict] = None 
