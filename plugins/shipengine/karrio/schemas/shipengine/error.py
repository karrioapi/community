import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Error:
    message: str
    error_source: str
    error_type: str
    error_code: str
    detail_code: typing.Optional[str] = None
    field_name: typing.Optional[str] = None
    field_value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    request_id: str
    errors: typing.List[Error] = jstruct.JList[Error] 
