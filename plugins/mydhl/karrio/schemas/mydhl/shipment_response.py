import attr
import jstruct
import typing

@attr.s(auto_attribs=True)
class ShipmentResponseType:
    url: typing.Optional[str] = None
    shipmentTrackingNumber: typing.Optional[str] = None
