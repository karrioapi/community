import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressType:
    type: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HouseNumberType:
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressDividedPropertiesType:
    housenumber: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    street: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]


@attr.s(auto_attribs=True)
class AddressDividedType:
    type: typing.Optional[str] = None
    properties: typing.Optional[AddressDividedPropertiesType] = jstruct.JStruct[AddressDividedPropertiesType]


@attr.s(auto_attribs=True)
class CountryPropertiesType:
    iso2: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    iso3: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    name: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]


@attr.s(auto_attribs=True)
class CountryType:
    type: typing.Optional[str] = None
    properties: typing.Optional[CountryPropertiesType] = jstruct.JStruct[CountryPropertiesType]


@attr.s(auto_attribs=True)
class CustomsDeclarationPropertiesType:
    eorinumber: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    license: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    certificate: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    invoice: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]


@attr.s(auto_attribs=True)
class CustomsDeclarationType:
    type: typing.Optional[str] = None
    properties: typing.Optional[CustomsDeclarationPropertiesType] = jstruct.JStruct[CustomsDeclarationPropertiesType]


@attr.s(auto_attribs=True)
class CustomsShipmentTypePropertiesType:
    id: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    name: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]


@attr.s(auto_attribs=True)
class CustomsShipmentTypeObjectType:
    type: typing.Optional[typing.List[str]] = None
    properties: typing.Optional[CustomsShipmentTypePropertiesType] = jstruct.JStruct[CustomsShipmentTypePropertiesType]


@attr.s(auto_attribs=True)
class DateCreatedType:
    type: typing.Optional[str] = None
    format: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PurplePropertiesType:
    type: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    size: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    link: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]


@attr.s(auto_attribs=True)
class DocumentsItemsType:
    type: typing.Optional[str] = None
    properties: typing.Optional[PurplePropertiesType] = jstruct.JStruct[PurplePropertiesType]


@attr.s(auto_attribs=True)
class DocumentsType:
    type: typing.Optional[str] = None
    items: typing.Optional[DocumentsItemsType] = jstruct.JStruct[DocumentsItemsType]


@attr.s(auto_attribs=True)
class NormalPrinterType:
    type: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class LabelPropertiesType:
    labelprinter: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    normalprinter: typing.Optional[NormalPrinterType] = jstruct.JStruct[NormalPrinterType]


@attr.s(auto_attribs=True)
class LabelType:
    type: typing.Optional[str] = None
    properties: typing.Optional[LabelPropertiesType] = jstruct.JStruct[LabelPropertiesType]


@attr.s(auto_attribs=True)
class FluffyPropertiesType:
    description: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    quantity: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    weight: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    value: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    hscode: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    origincountry: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    sku: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    productid: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]


@attr.s(auto_attribs=True)
class ParcelItemsItemsType:
    type: typing.Optional[str] = None
    properties: typing.Optional[FluffyPropertiesType] = jstruct.JStruct[FluffyPropertiesType]


@attr.s(auto_attribs=True)
class ParcelItemsType:
    type: typing.Optional[str] = None
    description: typing.Optional[str] = None
    items: typing.Optional[ParcelItemsItemsType] = jstruct.JStruct[ParcelItemsItemsType]


@attr.s(auto_attribs=True)
class ShipmentType:
    type: typing.Optional[str] = None
    properties: typing.Optional[CustomsShipmentTypePropertiesType] = jstruct.JStruct[CustomsShipmentTypePropertiesType]


@attr.s(auto_attribs=True)
class StatusPropertiesType:
    id: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]
    message: typing.Optional[HouseNumberType] = jstruct.JStruct[HouseNumberType]


@attr.s(auto_attribs=True)
class StatusType:
    type: typing.Optional[str] = None
    properties: typing.Optional[StatusPropertiesType] = jstruct.JStruct[StatusPropertiesType]


@attr.s(auto_attribs=True)
class ToServicePointType:
    type: typing.Optional[typing.List[str]] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelPropertiesType:
    id: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    address2: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    addressdivided: typing.Optional[AddressDividedType] = jstruct.JStruct[AddressDividedType]
    city: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    companyname: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    country: typing.Optional[CountryType] = jstruct.JStruct[CountryType]
    datecreated: typing.Optional[DateCreatedType] = jstruct.JStruct[DateCreatedType]
    email: typing.Optional[DateCreatedType] = jstruct.JStruct[DateCreatedType]
    name: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    postalcode: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    reference: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    telephone: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    trackingnumber: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    weight: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    label: typing.Optional[LabelType] = jstruct.JStruct[LabelType]
    customsdeclaration: typing.Optional[CustomsDeclarationType] = jstruct.JStruct[CustomsDeclarationType]
    ordernumber: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    insuredvalue: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    totalinsuredvalue: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    toservicepoint: typing.Optional[ToServicePointType] = jstruct.JStruct[ToServicePointType]
    customsinvoicenr: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    customsshipmenttype: typing.Optional[CustomsShipmentTypeObjectType] = jstruct.JStruct[CustomsShipmentTypeObjectType]
    parcelitems: typing.Optional[ParcelItemsType] = jstruct.JStruct[ParcelItemsType]
    documents: typing.Optional[DocumentsType] = jstruct.JStruct[DocumentsType]


@attr.s(auto_attribs=True)
class ParcelType:
    type: typing.Optional[str] = None
    properties: typing.Optional[ParcelPropertiesType] = jstruct.JStruct[ParcelPropertiesType]
    required: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ShipmentResponsePropertiesType:
    parcel: typing.Optional[ParcelType] = jstruct.JStruct[ParcelType]


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    type: typing.Optional[str] = None
    properties: typing.Optional[ShipmentResponsePropertiesType] = jstruct.JStruct[ShipmentResponsePropertiesType]
    required: typing.Optional[typing.List[str]] = None
