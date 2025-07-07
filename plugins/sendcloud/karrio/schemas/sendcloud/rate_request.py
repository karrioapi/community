import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class RateRequestType:
    fromcountry: typing.Optional[str] = None
    tocountry: typing.Optional[str] = None
    frompostalcode: typing.Optional[str] = None
    topostalcode: typing.Optional[int] = None
    weight: typing.Optional[float] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    isreturn: typing.Optional[bool] = None
    requestlabelasync: typing.Optional[bool] = None
