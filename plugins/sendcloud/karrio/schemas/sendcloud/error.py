import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    request: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorsType:
    fromcountry: typing.Optional[typing.List[str]] = None
    weight: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    error: typing.Optional[ErrorType] = jstruct.JStruct[ErrorType]
    errors: typing.Optional[ErrorsType] = jstruct.JStruct[ErrorsType]
