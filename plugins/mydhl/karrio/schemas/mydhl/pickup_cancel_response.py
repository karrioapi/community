import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupCancelResponseType:
    message: typing.Optional[str] = None
