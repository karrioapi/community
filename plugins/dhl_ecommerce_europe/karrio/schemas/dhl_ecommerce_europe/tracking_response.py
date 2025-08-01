import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingEvent:
    timestamp: typing.Optional[str] = None
    eventCode: typing.Optional[str] = None
    eventDescription: typing.Optional[str] = None
    location: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingInfo:
    trackingNumber: typing.Optional[str] = None
    status: typing.Optional[str] = None
    estimatedDeliveryDate: typing.Optional[str] = None
    actualDeliveryDate: typing.Optional[str] = None
    events: typing.Optional[typing.List[TrackingEvent]] = jstruct.JList[TrackingEvent]


@attr.s(auto_attribs=True)
class TrackingBody:
    trackingInfos: typing.Optional[typing.List[TrackingInfo]] = jstruct.JList[TrackingInfo]


@attr.s(auto_attribs=True)
class TrackingHeader:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    header: typing.Optional[TrackingHeader] = jstruct.JStruct[TrackingHeader]
    body: typing.Optional[TrackingBody] = jstruct.JStruct[TrackingBody] 
