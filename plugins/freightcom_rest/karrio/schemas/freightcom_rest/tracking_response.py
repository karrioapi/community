import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class WhereType:
    city: typing.Optional[str] = None
    region: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EventType:
    type: typing.Optional[str] = None
    when: typing.Optional[str] = None
    where: typing.Optional[WhereType] = jstruct.JStruct[WhereType]
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
