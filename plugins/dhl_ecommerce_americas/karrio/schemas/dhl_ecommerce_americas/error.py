import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorHeaderType:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None
    messageDetail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorDetailType:
    errorCode: typing.Optional[str] = None
    errorMessage: typing.Optional[str] = None
    errorDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorBodyType:
    errors: typing.Optional[typing.List[ErrorDetailType]] = jstruct.JList[ErrorDetailType]


@attr.s(auto_attribs=True)
class ErrorResponseType:
    header: typing.Optional[ErrorHeaderType] = jstruct.JStruct[ErrorHeaderType]
    body: typing.Optional[ErrorBodyType] = jstruct.JStruct[ErrorBodyType]