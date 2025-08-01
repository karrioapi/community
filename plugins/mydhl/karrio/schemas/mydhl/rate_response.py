import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TotalPriceType:
    currencyType: typing.Optional[str] = None
    priceCurrency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryCapabilitiesType:
    deliveryTypeCode: typing.Optional[str] = None
    estimatedDeliveryDateAndTime: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ProductType:
    productName: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
    totalPrice: typing.Optional[typing.List[TotalPriceType]] = jstruct.JList[TotalPriceType]
    deliveryCapabilities: typing.Optional[DeliveryCapabilitiesType] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    products: typing.Optional[typing.List[ProductType]] = jstruct.JList[ProductType]
