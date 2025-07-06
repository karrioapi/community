import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class NormalizedAddressType:
    street_address: typing.Optional[str] = None
    city_locality: typing.Optional[str] = None
    postal_code: typing.Optional[int] = None
    country_code: typing.Optional[str] = None
    state_province: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValidationMessageType:
    message: typing.Optional[str] = None
    code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressValidationResponseType:
    is_valid: typing.Optional[bool] = None
    normalized_address: typing.Optional[NormalizedAddressType] = jstruct.JStruct[NormalizedAddressType]
    validation_messages: typing.Optional[typing.List[ValidationMessageType]] = jstruct.JList[ValidationMessageType]
