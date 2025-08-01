import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class RateRequestType:
    to_country: typing.Optional[str] = None
    to_postal_code: typing.Optional[str] = None
    from_country: typing.Optional[str] = None
    from_postal_code: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    weight_unit: typing.Optional[str] = None
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    declared_value: typing.Optional[float] = None
    declared_value_currency: typing.Optional[str] = None
    service_point_id: typing.Optional[str] = None
