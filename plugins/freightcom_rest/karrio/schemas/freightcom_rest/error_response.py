import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DataType:
    services: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    message: typing.Optional[str] = None
    data: typing.Optional[DataType] = jstruct.JStruct[DataType]
