import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelRequestType:
    label_id: typing.Optional[str] = None
