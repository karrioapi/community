import attr
import typing

@attr.s(auto_attribs=True)
class RateResponseType:
    rates: typing.Optional[typing.List] = None
