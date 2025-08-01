import attr
import typing

@attr.s(auto_attribs=True)
class RateRequestType:
    origin_postal_code: typing.Optional[str] = None
    destination_postal_code: typing.Optional[str] = None
