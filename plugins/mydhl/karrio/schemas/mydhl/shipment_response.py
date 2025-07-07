import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DocumentType:
    imageFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EstimatedDeliveryDateType:
    estimatedDeliveryDate: typing.Optional[str] = None
    estimatedDeliveryType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    referenceNumber: typing.Optional[int] = None
    trackingNumber: typing.Optional[str] = None
    trackingUrl: typing.Optional[str] = None
    volumetricWeight: typing.Optional[float] = None
    documents: typing.Optional[typing.List[DocumentType]] = jstruct.JList[DocumentType]


@attr.s(auto_attribs=True)
class ContactInformationType:
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    mobilePhone: typing.Optional[str] = None
    companyName: typing.Optional[str] = None
    fullName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PostalAddressType:
    postalCode: typing.Optional[int] = None
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    provinceCode: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    addressLine3: typing.Optional[str] = None
    countyName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RegistrationNumberType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[str] = None
    issuerCountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErDetailsType:
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    contactInformation: typing.Optional[ContactInformationType] = jstruct.JStruct[ContactInformationType]
    registrationNumbers: typing.Optional[typing.List[RegistrationNumberType]] = jstruct.JList[RegistrationNumberType]
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[ErDetailsType] = jstruct.JStruct[ErDetailsType]
    receiverDetails: typing.Optional[ErDetailsType] = jstruct.JStruct[ErDetailsType]


@attr.s(auto_attribs=True)
class ShipmentDetailType:
    serviceHandlingFeatureCodes: typing.Optional[typing.List[str]] = None
    volumetricWeight: typing.Optional[float] = None
    billingCode: typing.Optional[str] = None
    serviceContentCode: typing.Optional[str] = None
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    shipmentTrackingNumber: typing.Optional[int] = None
    cancelPickupUrl: typing.Optional[str] = None
    trackingUrl: typing.Optional[str] = None
    dispatchConfirmationNumber: typing.Optional[str] = None
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    documents: typing.Optional[typing.List[DocumentType]] = jstruct.JList[DocumentType]
    onDemandDeliveryURL: typing.Optional[str] = None
    shipmentDetails: typing.Optional[typing.List[ShipmentDetailType]] = jstruct.JList[ShipmentDetailType]
    estimatedDeliveryDate: typing.Optional[EstimatedDeliveryDateType] = jstruct.JStruct[EstimatedDeliveryDateType]
    warnings: typing.Optional[typing.List[str]] = None
