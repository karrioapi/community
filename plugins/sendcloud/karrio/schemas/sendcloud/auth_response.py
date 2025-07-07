import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AuthResponseType:
    accesstoken: typing.Optional[str] = None
    expiresin: typing.Optional[int] = None
    idtoken: typing.Any = None
    refreshtoken: typing.Optional[str] = None
    scope: typing.Optional[str] = None
    tokentype: typing.Optional[str] = None
