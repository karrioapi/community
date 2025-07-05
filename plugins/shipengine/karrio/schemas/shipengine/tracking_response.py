import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingEvent:
    occurred_at: str
    carrier_occurred_at: str
    description: str
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    company_name: typing.Optional[str] = None
    signer: typing.Optional[str] = None
    event_code: typing.Optional[str] = None
    status_code: typing.Optional[str] = None
    status_description: typing.Optional[str] = None
    carrier_status_code: typing.Optional[str] = None
    carrier_detail_code: typing.Optional[str] = None
    carrier_status_description: typing.Optional[str] = None
    carrier_detail_description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    tracking_number: str
    status_code: str
    status_description: str
    carrier_status_code: str
    carrier_status_description: str
    carrier_detail_code: typing.Optional[str] = None
    carrier_detail_description: typing.Optional[str] = None
    ship_date: typing.Optional[str] = None
    estimated_delivery_date: typing.Optional[str] = None
    actual_delivery_date: typing.Optional[str] = None
    exception_description: typing.Optional[str] = None
    events: typing.List[TrackingEvent] = jstruct.JList[TrackingEvent] 
