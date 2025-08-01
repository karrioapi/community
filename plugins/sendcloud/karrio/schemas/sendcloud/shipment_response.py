import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelType:
    label_printer: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServicePointType:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StatusType:
    id: typing.Optional[int] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelResponseType:
    id: typing.Optional[int] = None
    tracking_number: typing.Optional[str] = None
    status: typing.Optional[StatusType] = None
    label: typing.Optional[LabelType] = None
    service_point: typing.Optional[ServicePointType] = None
    carrier: typing.Optional[dict] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    parcel: typing.Optional[ParcelResponseType] = None
