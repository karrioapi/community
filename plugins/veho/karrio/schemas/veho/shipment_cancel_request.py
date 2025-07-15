import attr
import typing


@attr.s(auto_attribs=True)
class ShipmentCancelRequest:
    """Veho Shipment Cancel Request"""
    
    shipmentIdentifier: typing.Optional[str] = None 
