import attr
import jstruct
import typing

@attr.s(auto_attribs=True)
class ShipmentRequestType:
    plannedShippingDateAndTime: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
