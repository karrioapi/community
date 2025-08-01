import attr
import jstruct
import typing
from karrio.schemas.sendcloud.shipment_response import StatusType


@attr.s(auto_attribs=True)
class TrackingEventType:
    status_id: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    message: typing.Optional[str] = None
    location: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingParcelType:
    id: typing.Optional[int] = None
    tracking_number: typing.Optional[str] = None
    status: typing.Optional[StatusType] = None
    tracking_events: typing.Optional[typing.List[TrackingEventType]] = jstruct.JList[TrackingEventType]
    carrier: typing.Optional[dict] = None
    service_point: typing.Optional[dict] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    parcels: typing.Optional[typing.List[TrackingParcelType]] = jstruct.JList[TrackingParcelType]
