import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorDetail:
    errorCode: typing.Optional[str] = None
    errorMessage: typing.Optional[str] = None
    errorDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorBody:
    errors: typing.Optional[typing.List[ErrorDetail]] = jstruct.JList[ErrorDetail]


@attr.s(auto_attribs=True)
class ErrorHeader:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None
    messageDetail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    header: typing.Optional[ErrorHeader] = jstruct.JStruct[ErrorHeader]
    body: typing.Optional[ErrorBody] = jstruct.JStruct[ErrorBody] 
