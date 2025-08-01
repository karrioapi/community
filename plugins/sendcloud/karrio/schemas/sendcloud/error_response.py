import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    error: typing.Optional[ErrorType] = None
    errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
