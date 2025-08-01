import attr
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelResponse:
    """Veho Shipment Cancel Response"""
    
    success: typing.Optional[bool] = None
    message: typing.Optional[str] = None 
