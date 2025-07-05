"""
SendCloud API v2/v3 Parcel Response Schema

Based on: https://panel.sendcloud.sc/api/v2/parcels
"""
import attr
import jstruct
import typing
import json


@attr.s(auto_attribs=True)
class Country:
    """Country information"""
    iso_2: str
    iso_3: str
    name: str


@attr.s(auto_attribs=True)
class Status:
    """Parcel status information"""
    id: int
    message: str


@attr.s(auto_attribs=True)
class Carrier:
    """Carrier information"""
    code: str


@attr.s(auto_attribs=True)
class Label:
    """Label download URLs"""
    normal_printer: typing.Optional[typing.List[str]] = jstruct.JList[str]
    label_printer: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressDivided:
    """Divided address components"""
    street: str
    house_number: str


@attr.s(auto_attribs=True)
class ParcelItemResponse:
    """Individual item in parcel response"""
    description: str
    quantity: int
    weight: str
    value: str
    hs_code: typing.Optional[str] = None
    origin_country: typing.Optional[str] = None
    product_id: typing.Optional[str] = None
    properties: typing.Optional[typing.Dict[str, typing.Any]] = None
    sku: typing.Optional[str] = None
    return_reason: typing.Optional[str] = None
    return_message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Document:
    """Document information"""
    type: str
    size: str
    link: str


@attr.s(auto_attribs=True)
class Shipment:
    id: int
    name: str


@attr.s(auto_attribs=True)
class Parcel:
    id: int
    address: str
    city: str
    email: str
    name: str
    postal_code: str
    telephone: str
    weight: str
    address_2: typing.Optional[str] = None
    address_divided: typing.Optional[AddressDivided] = jstruct.JStruct[AddressDivided]
    company_name: typing.Optional[str] = None
    country: typing.Optional[Country] = jstruct.JStruct[Country]
    data: typing.Optional[typing.Dict[str, typing.Any]] = None
    date_created: typing.Optional[str] = None
    date_announced: typing.Optional[str] = None
    date_updated: typing.Optional[str] = None
    reference: typing.Optional[str] = None
    shipment: typing.Optional[Shipment] = jstruct.JStruct[Shipment]
    status: typing.Optional[Status] = jstruct.JStruct[Status]
    to_service_point: typing.Optional[int] = None
    tracking_number: typing.Optional[str] = None
    label: typing.Optional[Label] = jstruct.JStruct[Label]
    customs_declaration: typing.Optional[typing.Dict[str, typing.Any]] = None
    order_number: typing.Optional[str] = None
    insured_value: typing.Optional[float] = None
    total_insured_value: typing.Optional[float] = None
    to_state: typing.Optional[str] = None
    customs_invoice_nr: typing.Optional[str] = None
    customs_shipment_type: typing.Optional[int] = None
    parcel_items: typing.Optional[typing.List[ParcelItemResponse]] = jstruct.JList[ParcelItemResponse]
    documents: typing.Optional[typing.List[Document]] = jstruct.JList[Document]
    type: typing.Optional[str] = None
    shipment_uuid: typing.Optional[str] = None
    shipping_method: typing.Optional[int] = None
    external_order_id: typing.Optional[str] = None
    external_shipment_id: typing.Optional[str] = None
    external_reference: typing.Optional[str] = None
    is_return: typing.Optional[bool] = None
    note: typing.Optional[str] = None
    to_post_number: typing.Optional[str] = None
    total_order_value: typing.Optional[str] = None
    total_order_value_currency: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    colli_uuid: typing.Optional[str] = None
    collo_nr: typing.Optional[int] = None
    collo_count: typing.Optional[int] = None
    awb_tracking_number: typing.Optional[str] = None
    box_number: typing.Optional[str] = None
    length: typing.Optional[str] = None
    width: typing.Optional[str] = None
    height: typing.Optional[str] = None
    shipping_method_checkout_name: typing.Optional[str] = None
    carrier: typing.Optional[Carrier] = jstruct.JStruct[Carrier]
    tracking_url: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelResponse:
    """Top-level parcel response wrapper"""
    parcel: Parcel = jstruct.JStruct[Parcel]
    
    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> 'ParcelResponse':
        """Create from dictionary (JSON deserialization)"""
        parcel_data = data['parcel']
        
        # Convert nested objects
        if 'country' in parcel_data:
            country_data = parcel_data['country']
            parcel_data['country'] = Country(**country_data)
        
        if 'status' in parcel_data:
            status_data = parcel_data['status']
            parcel_data['status'] = Status(**status_data)
            
        if 'carrier' in parcel_data and parcel_data['carrier']:
            carrier_data = parcel_data['carrier']
            parcel_data['carrier'] = Carrier(**carrier_data)
            
        if 'address_divided' in parcel_data and parcel_data['address_divided']:
            addr_data = parcel_data['address_divided']
            parcel_data['address_divided'] = AddressDivided(**addr_data)
            
        if 'shipment' in parcel_data and parcel_data['shipment']:
            shipment_data = parcel_data['shipment']
            parcel_data['shipment'] = Shipment(**shipment_data)
            
        if 'label' in parcel_data and parcel_data['label']:
            label_data = parcel_data['label']
            parcel_data['label'] = Label(**label_data)
            
        # Convert parcel items
        if 'parcel_items' in parcel_data:
            items = []
            for item_data in parcel_data['parcel_items']:
                items.append(ParcelItemResponse(**item_data))
            parcel_data['parcel_items'] = items
            
        # Convert documents
        if 'documents' in parcel_data:
            docs = []
            for doc_data in parcel_data['documents']:
                docs.append(Document(**doc_data))
            parcel_data['documents'] = docs
        
        return cls(parcel=Parcel(**parcel_data))
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ParcelResponse':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)


# Error response
@attr.s(auto_attribs=True)
class ErrorResponse:
    """Error response from SendCloud API"""
    error: typing.Dict[str, typing.Any]
    
    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> 'ErrorResponse':
        return cls(error=data.get('error', data))
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ErrorResponse':
        data = json.loads(json_str)
        return cls.from_dict(data) 
