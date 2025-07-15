import attr
import typing


@attr.s(auto_attribs=True)
class LabelData:
    """Veho Label Data structure"""
    
    format: typing.Optional[str] = None
    image: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentData:
    """Veho Shipment Data structure"""
    
    trackingNumber: typing.Optional[str] = None
    shipmentId: typing.Optional[str] = None
    labelData: typing.Optional[LabelData] = None
    invoiceImage: typing.Optional[str] = None
    serviceCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponse:
    """Veho Shipment Response containing shipment object"""
    
    shipment: typing.Optional[ShipmentData] = None
