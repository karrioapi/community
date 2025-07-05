import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequest:
    tracking_number: typing.Optional[str] = None
    parcel_id: typing.Optional[int] = None 
