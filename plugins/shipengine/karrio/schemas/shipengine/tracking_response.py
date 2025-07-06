import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EventType:
    occurred_at: typing.Optional[str] = None
    description: typing.Optional[str] = None
    event_code: typing.Optional[str] = None
    city_locality: typing.Optional[str] = None
    state_province: typing.Optional[str] = None
    country_code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    tracking_number: typing.Optional[str] = None
    status_code: typing.Optional[str] = None
    status_description: typing.Optional[str] = None
    carrier_code: typing.Optional[str] = None
    carrier_status_description: typing.Optional[str] = None
    estimated_delivery_date: typing.Optional[str] = None
    actual_delivery_date: typing.Optional[str] = None
    tracking_url: typing.Optional[str] = None
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
