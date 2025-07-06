import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressValidationRequestType:
    street_address: typing.Optional[str] = None
    city_locality: typing.Optional[str] = None
    postal_code: typing.Optional[int] = None
    country_code: typing.Optional[str] = None
    state_province: typing.Optional[str] = None
