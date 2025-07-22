import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Charge:
    chargeType: typing.Optional[str] = None
    chargeAmount: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class Rate:
    productCode: typing.Optional[str] = None
    productName: typing.Optional[str] = None
    totalCharge: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    transitTime: typing.Optional[int] = None
    deliveryGuarantee: typing.Optional[bool] = None
    charges: typing.Optional[typing.List[Charge]] = jstruct.JList[Charge]


@attr.s(auto_attribs=True)
class RateBody:
    rates: typing.Optional[typing.List[Rate]] = jstruct.JList[Rate]


@attr.s(auto_attribs=True)
class RateHeader:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateResponse:
    header: typing.Optional[RateHeader] = jstruct.JStruct[RateHeader]
    body: typing.Optional[RateBody] = jstruct.JStruct[RateBody] 
