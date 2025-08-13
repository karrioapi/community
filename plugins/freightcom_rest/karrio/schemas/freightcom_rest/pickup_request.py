import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DateType:
    year: typing.Optional[int] = None
    month: typing.Optional[int] = None
    day: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ReadyType:
    hour: typing.Optional[int] = None
    minute: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DispatchDetailsType:
    date: typing.Optional[DateType] = jstruct.JStruct[DateType]
    ready_at: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    ready_until: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]


@attr.s(auto_attribs=True)
class ContactPhoneNumberType:
    number: typing.Optional[str] = None
    extension: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PickupDetailsType:
    pre_scheduled_pickup: typing.Optional[bool] = None
    date: typing.Optional[DateType] = jstruct.JStruct[DateType]
    ready_at: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    ready_until: typing.Optional[ReadyType] = jstruct.JStruct[ReadyType]
    pickup_location: typing.Optional[str] = None
    contact_name: typing.Optional[str] = None
    contact_phone_number: typing.Optional[ContactPhoneNumberType] = jstruct.JStruct[ContactPhoneNumberType]


@attr.s(auto_attribs=True)
class PickupRequestType:
    pickup_details: typing.Optional[PickupDetailsType] = jstruct.JStruct[PickupDetailsType]
    dispatch_details: typing.Optional[DispatchDetailsType] = jstruct.JStruct[DispatchDetailsType]
