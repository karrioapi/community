import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    error_source: typing.Optional[str] = None
    error_type: typing.Optional[str] = None
    error_code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    field_name: typing.Optional[str] = None
    field_value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
    request_id: typing.Optional[str] = None
