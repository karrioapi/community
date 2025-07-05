import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequest:
    carrier_code: str
    tracking_number: str 
