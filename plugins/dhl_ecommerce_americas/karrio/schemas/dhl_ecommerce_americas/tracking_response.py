import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingResponseHeaderType:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None
    messageDetail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingEventType:
    eventDate: typing.Optional[str] = None
    eventTime: typing.Optional[str] = None
    eventDescription: typing.Optional[str] = None
    location: typing.Optional[str] = None
    eventCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseBodyType:
    trackingNumber: typing.Optional[str] = None
    status: typing.Optional[str] = None
    events: typing.Optional[typing.List[TrackingEventType]] = jstruct.JList[TrackingEventType]
    deliveryDate: typing.Optional[str] = None
    deliveryTime: typing.Optional[str] = None
    signedBy: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    header: typing.Optional[TrackingResponseHeaderType] = jstruct.JStruct[TrackingResponseHeaderType]
    body: typing.Optional[TrackingResponseBodyType] = jstruct.JStruct[TrackingResponseBodyType]
