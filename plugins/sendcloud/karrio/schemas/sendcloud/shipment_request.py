import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ParcelItemType:
    description: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    weight: typing.Optional[str] = None
    value: typing.Optional[str] = None
    hscode: typing.Optional[str] = None
    origincountry: typing.Optional[str] = None
    sku: typing.Optional[str] = None
    productid: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    name: typing.Optional[str] = None
    address: typing.Optional[str] = None
    address2: typing.Optional[str] = None
    housenumber: typing.Optional[int] = None
    city: typing.Optional[str] = None
    postalcode: typing.Optional[str] = None
    country: typing.Optional[str] = None
    companyname: typing.Optional[str] = None
    email: typing.Optional[str] = None
    telephone: typing.Optional[str] = None
    weight: typing.Optional[str] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    requestlabel: typing.Optional[bool] = None
    applyshippingrules: typing.Optional[bool] = None
    shippingmethod: typing.Optional[int] = None
    externalreference: typing.Optional[str] = None
    ordernumber: typing.Optional[str] = None
    insuredvalue: typing.Optional[float] = None
    totalinsuredvalue: typing.Optional[float] = None
    senderaddress: typing.Optional[int] = None
    shipmentuuid: typing.Optional[str] = None
    customsinvoicenr: typing.Optional[str] = None
    customsshipmenttype: typing.Optional[int] = None
    parcelitems: typing.Optional[typing.List[ParcelItemType]] = jstruct.JList[ParcelItemType]
