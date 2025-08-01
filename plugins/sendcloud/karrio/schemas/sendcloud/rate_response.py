import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PriceType:
    value: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CarrierType:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingMethodType:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None
    price: typing.Optional[PriceType] = None
    transit_time_days: typing.Optional[int] = None
    carrier: typing.Optional[CarrierType] = None
    cost_breakdown: typing.Optional[dict] = None
    min_weight: typing.Optional[float] = None
    max_weight: typing.Optional[float] = None
    countries: typing.Optional[typing.List[str]] = jstruct.JList[str]
    properties: typing.Optional[dict] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    shipping_methods: typing.Optional[typing.List[ShippingMethodType]] = jstruct.JList[ShippingMethodType]
