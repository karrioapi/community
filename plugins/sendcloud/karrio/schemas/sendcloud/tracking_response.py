import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CodeType:
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CarrierPropertiesType:
    code: typing.Optional[CodeType] = jstruct.JStruct[CodeType]
    name: typing.Optional[CodeType] = jstruct.JStruct[CodeType]


@attr.s(auto_attribs=True)
class CarrierType:
    type: typing.Optional[str] = None
    properties: typing.Optional[CarrierPropertiesType] = jstruct.JStruct[CarrierPropertiesType]


@attr.s(auto_attribs=True)
class DateCreatedType:
    type: typing.Optional[str] = None
    format: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class IDType:
    type: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentPropertiesType:
    id: typing.Optional[CodeType] = jstruct.JStruct[CodeType]
    name: typing.Optional[CodeType] = jstruct.JStruct[CodeType]


@attr.s(auto_attribs=True)
class ShipmentType:
    type: typing.Optional[str] = None
    properties: typing.Optional[ShipmentPropertiesType] = jstruct.JStruct[ShipmentPropertiesType]


@attr.s(auto_attribs=True)
class StatusPropertiesType:
    id: typing.Optional[CodeType] = jstruct.JStruct[CodeType]
    message: typing.Optional[CodeType] = jstruct.JStruct[CodeType]


@attr.s(auto_attribs=True)
class StatusType:
    type: typing.Optional[str] = None
    properties: typing.Optional[StatusPropertiesType] = jstruct.JStruct[StatusPropertiesType]


@attr.s(auto_attribs=True)
class LocationPropertiesType:
    country: typing.Optional[CodeType] = jstruct.JStruct[CodeType]
    state: typing.Optional[CodeType] = jstruct.JStruct[CodeType]
    city: typing.Optional[CodeType] = jstruct.JStruct[CodeType]
    postalcode: typing.Optional[CodeType] = jstruct.JStruct[CodeType]


@attr.s(auto_attribs=True)
class LocationType:
    type: typing.Optional[str] = None
    properties: typing.Optional[LocationPropertiesType] = jstruct.JStruct[LocationPropertiesType]


@attr.s(auto_attribs=True)
class TimestampType:
    type: typing.Optional[str] = None
    format: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemsPropertiesType:
    message: typing.Optional[CodeType] = jstruct.JStruct[CodeType]
    timestamp: typing.Optional[TimestampType] = jstruct.JStruct[TimestampType]
    status: typing.Optional[CodeType] = jstruct.JStruct[CodeType]
    carrier: typing.Optional[CodeType] = jstruct.JStruct[CodeType]
    location: typing.Optional[LocationType] = jstruct.JStruct[LocationType]


@attr.s(auto_attribs=True)
class ItemsType:
    type: typing.Optional[str] = None
    properties: typing.Optional[ItemsPropertiesType] = jstruct.JStruct[ItemsPropertiesType]


@attr.s(auto_attribs=True)
class TrackingEventsType:
    type: typing.Optional[str] = None
    items: typing.Optional[ItemsType] = jstruct.JStruct[ItemsType]


@attr.s(auto_attribs=True)
class ParcelPropertiesType:
    id: typing.Optional[IDType] = jstruct.JStruct[IDType]
    trackingnumber: typing.Optional[IDType] = jstruct.JStruct[IDType]
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    datecreated: typing.Optional[DateCreatedType] = jstruct.JStruct[DateCreatedType]
    trackingurl: typing.Optional[DateCreatedType] = jstruct.JStruct[DateCreatedType]
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
    carrier: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    trackingevents: typing.Optional[TrackingEventsType] = jstruct.JStruct[TrackingEventsType]


@attr.s(auto_attribs=True)
class ParcelType:
    type: typing.Optional[str] = None
    properties: typing.Optional[ParcelPropertiesType] = jstruct.JStruct[ParcelPropertiesType]
    required: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class TrackingResponsePropertiesType:
    parcel: typing.Optional[ParcelType] = jstruct.JStruct[ParcelType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    type: typing.Optional[str] = None
    properties: typing.Optional[TrackingResponsePropertiesType] = jstruct.JStruct[TrackingResponsePropertiesType]
    required: typing.Optional[typing.List[str]] = None
