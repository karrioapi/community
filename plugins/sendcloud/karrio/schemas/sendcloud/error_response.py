import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorDetail:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    field: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    error: typing.Dict[str, typing.Any]
    message: typing.Optional[str] = None
    errors: typing.Optional[typing.List[ErrorDetail]] = jstruct.JList[ErrorDetail] 
