import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressType:
    street1: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zip: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LocationType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class ItemType:
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    quantity: typing.Optional[int] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class DeliverBetweenType:
    start: typing.Optional[str] = None
    end: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateRequestType:
    items: typing.Optional[typing.List[ItemType]] = jstruct.JStruct[ItemType]
    pickup_location: typing.Optional[LocationType] = jstruct.JStruct[LocationType]
    delivery_location: typing.Optional[LocationType] = jstruct.JStruct[LocationType]
    pickup_after: typing.Optional[str] = None
    deliver_between: typing.Optional[DeliverBetweenType] = jstruct.JStruct[DeliverBetweenType]