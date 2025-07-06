import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AmountType:
    amount: typing.Optional[str] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateType:
    rate_id: typing.Optional[str] = None
    carrier_id: typing.Optional[str] = None
    carrier_code: typing.Optional[str] = None
    service_code: typing.Optional[str] = None
    service_type: typing.Optional[str] = None
    carrier_friendly_name: typing.Optional[str] = None
    shipping_amount: typing.Optional[AmountType] = jstruct.JStruct[AmountType]
    insurance_amount: typing.Optional[AmountType] = jstruct.JStruct[AmountType]
    confirmation_amount: typing.Optional[AmountType] = jstruct.JStruct[AmountType]
    other_amount: typing.Optional[AmountType] = jstruct.JStruct[AmountType]
    delivery_days: typing.Optional[int] = None
    estimated_delivery_date: typing.Optional[str] = None
    guaranteed_service: typing.Optional[bool] = None
    trackable: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class RateResponseClassType:
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]


@attr.s(auto_attribs=True)
class RateResponseType:
    rate_response: typing.Optional[RateResponseClassType] = jstruct.JStruct[RateResponseClassType]
