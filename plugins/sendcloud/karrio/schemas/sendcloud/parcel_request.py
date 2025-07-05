"""
SendCloud API v2/v3 Parcel Request Schema

Based on: https://panel.sendcloud.sc/api/v2/parcels
"""
import attr
import jstruct
import typing
import json


@attr.s(auto_attribs=True)
class ParcelItem:
    """Individual item within a parcel"""
    description: str
    quantity: int
    weight: str  # Weight in kg as string
    value: str  # Value as string
    hs_code: typing.Optional[str] = None
    origin_country: typing.Optional[str] = None
    product_id: typing.Optional[str] = None
    sku: typing.Optional[str] = None
    properties: typing.Optional[typing.Dict[str, typing.Any]] = None


@attr.s(auto_attribs=True)
class Shipment:
    """Shipment method selection"""
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelData:
    """Main parcel data structure"""
    # Recipient information
    name: str
    email: str
    telephone: str
    address: str
    house_number: str
    city: str
    country: str
    postal_code: str
    
    # Package dimensions
    weight: str  # Total weight in kg as string
    length: typing.Optional[str] = None  # cm as string
    width: typing.Optional[str] = None  # cm as string  
    height: typing.Optional[str] = None  # cm as string
    
    # Optional fields
    company_name: typing.Optional[str] = None
    address_2: typing.Optional[str] = None
    country_state: typing.Optional[str] = None
    
    # Items
    parcel_items: typing.List[ParcelItem] = jstruct.JList[ParcelItem]
    
    # Shipment details
    shipment: typing.Optional[Shipment] = jstruct.JStruct[Shipment]
    sender_address: typing.Optional[int] = None
    
    # Order details
    total_order_value: typing.Optional[str] = None
    total_order_value_currency: typing.Optional[str] = None
    
    # Service options
    quantity: typing.Optional[int] = None
    total_insured_value: typing.Optional[float] = None
    is_return: typing.Optional[bool] = None
    request_label: typing.Optional[bool] = None
    apply_shipping_rules: typing.Optional[bool] = None
    request_label_async: typing.Optional[bool] = None
    
    # Optional service point
    to_service_point: typing.Optional[int] = None
    to_post_number: typing.Optional[str] = None
    
    # Customs
    customs_invoice_nr: typing.Optional[str] = None
    customs_shipment_type: typing.Optional[int] = None
    
    # Additional
    shipping_method_checkout_name: typing.Optional[str] = None
    external_order_id: typing.Optional[str] = None
    note: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelRequest:
    """Top-level parcel request wrapper"""
    parcel: ParcelData = jstruct.JStruct[ParcelData]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""

        def convert_dataclass(obj):
            if hasattr(obj, '__dataclass_fields__'):
                result = {}
                for field_name, field_value in obj.__dict__.items():
                    if field_value is not None:
                        if hasattr(field_value, '__dataclass_fields__'):
                            result[field_name] = convert_dataclass(field_value)
                        elif isinstance(field_value, list):
                            result[field_name] = [
                                convert_dataclass(item) if hasattr(item, '__dataclass_fields__') else item
                                for item in field_value
                            ]
                        else:
                            result[field_name] = field_value
                return result
            return obj
        
        return convert_dataclass(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


# Convenience functions for creating requests
def create_parcel_request(
    # Recipient
    name: str,
    email: str,
    telephone: str,
    address: str,
    house_number: str,
    city: str,
    country: str,
    postal_code: str,
    
    # Package
    weight: str,
    length: str=None,
    width: str=None,
    height: str=None,
    
    # Items
    parcel_items: typing.List[ParcelItem]=None,
    
    # Options
    shipment_id: int=None,
    shipment_name: str=None,
    request_label: bool=False,
    **kwargs
) -> ParcelRequest:
    """Create a parcel request with common parameters"""
    
    shipment = None
    if shipment_id and shipment_name:
        shipment = Shipment(id=shipment_id, name=shipment_name)
    
    parcel_data = ParcelData(
        name=name,
        email=email,
        telephone=telephone,
        address=address,
        house_number=house_number,
        city=city,
        country=country,
        postal_code=postal_code,
        weight=weight,
        length=length,
        width=width,
        height=height,
        parcel_items=parcel_items or [],
        shipment=shipment,
        request_label=request_label,
        **kwargs
    )
    
    return ParcelRequest(parcel=parcel_data) 
