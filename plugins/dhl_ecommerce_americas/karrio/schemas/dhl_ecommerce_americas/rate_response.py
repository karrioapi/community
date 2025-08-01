import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class HeaderType:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None
    messageDetail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ChargeType:
    chargeType: typing.Optional[str] = None
    chargeAmount: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class RateType:
    productCode: typing.Optional[str] = None
    productName: typing.Optional[str] = None
    totalCharge: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    transitTime: typing.Optional[int] = None
    deliveryGuarantee: typing.Optional[bool] = None
    charges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]


@attr.s(auto_attribs=True)
class BodyType:
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]


@attr.s(auto_attribs=True)
class RateResponseType:
    header: typing.Optional[HeaderType] = jstruct.JStruct[HeaderType]
    body: typing.Optional[BodyType] = jstruct.JStruct[BodyType]
