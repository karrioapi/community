from attr import define, field
from typing import Optional, List


@define
class ShipmentLabel:
    tracking_number: Optional[str] = None
    label_format: Optional[str] = None
    label_data: Optional[str] = None


@define
class ShipmentResponse:
    shipment_id: Optional[str] = None
    tracking_number: Optional[str] = None
    labels: Optional[List[ShipmentLabel]] = None
    total_charge: Optional[float] = None
    currency: Optional[str] = None
    service: Optional[str] = None
    errors: Optional[List[str]] = None 
