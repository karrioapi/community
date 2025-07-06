import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    tracking_numbers: typing.Optional[typing.List[str]] = None
    reference: typing.Optional[str] = None
