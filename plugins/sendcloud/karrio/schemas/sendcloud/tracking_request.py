import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CarrierType:
    type: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PropertiesType:
    trackingnumber: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    carrier: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]


@attr.s(auto_attribs=True)
class TrackingRequestType:
    type: typing.Optional[str] = None
    properties: typing.Optional[PropertiesType] = jstruct.JStruct[PropertiesType]
    required: typing.Optional[typing.List[str]] = None
