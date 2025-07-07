import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class AdditionalChargeType:
    value: typing.Optional[int] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerReferenceType:
    typeCode: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExporterType:
    id: typing.Optional[int] = None
    code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InvoiceType:
    number: typing.Optional[str] = None
    date: typing.Optional[str] = None
    function: typing.Optional[str] = None
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]


@attr.s(auto_attribs=True)
class QuantityType:
    value: typing.Optional[int] = None
    unitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    netValue: typing.Optional[int] = None
    grossValue: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class LineItemType:
    number: typing.Optional[int] = None
    description: typing.Optional[str] = None
    price: typing.Optional[int] = None
    quantity: typing.Optional[QuantityType] = jstruct.JStruct[QuantityType]
    commodityCodes: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    exportReasonType: typing.Optional[str] = None
    manufacturerCountry: typing.Optional[str] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    isTaxesPaid: typing.Optional[bool] = None
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    customsDocuments: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]


@attr.s(auto_attribs=True)
class RemarkType:
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExportDeclarationType:
    lineItems: typing.Optional[typing.List[LineItemType]] = jstruct.JList[LineItemType]
    invoice: typing.Optional[InvoiceType] = jstruct.JStruct[InvoiceType]
    remarks: typing.Optional[typing.List[RemarkType]] = jstruct.JList[RemarkType]
    additionalCharges: typing.Optional[typing.List[AdditionalChargeType]] = jstruct.JList[AdditionalChargeType]
    placeOfIncoterm: typing.Optional[str] = None
    recipientReference: typing.Optional[str] = None
    exporter: typing.Optional[ExporterType] = jstruct.JStruct[ExporterType]
    exportReasonType: typing.Optional[str] = None
    shipmentType: typing.Optional[str] = None
    customsDocuments: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BarcodeType:
    position: typing.Optional[str] = None
    symbologyCode: typing.Optional[int] = None
    content: typing.Optional[str] = None
    textBelowBarcode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelTextType:
    position: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    typeCode: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    description: typing.Optional[str] = None
    labelBarcodes: typing.Optional[typing.List[BarcodeType]] = jstruct.JList[BarcodeType]
    labelText: typing.Optional[typing.List[LabelTextType]] = jstruct.JList[LabelTextType]
    labelDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContentType:
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    isCustomsDeclarable: typing.Optional[bool] = None
    declaredValue: typing.Optional[int] = None
    declaredValueCurrency: typing.Optional[str] = None
    exportDeclaration: typing.Optional[ExportDeclarationType] = jstruct.JStruct[ExportDeclarationType]
    description: typing.Optional[str] = None
    USFilingTypeValue: typing.Optional[int] = None
    incoterm: typing.Optional[str] = None
    unitOfMeasurement: typing.Optional[str] = None


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
class DetailsType:
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    contactInformation: typing.Optional[ContactInformationType] = jstruct.JStruct[ContactInformationType]
    registrationNumbers: typing.Optional[typing.List[RegistrationNumberType]] = jstruct.JList[RegistrationNumberType]
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    receiverDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    buyerDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]


@attr.s(auto_attribs=True)
class DocumentImageType:
    typeCode: typing.Optional[str] = None
    imageFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None
    isRequested: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class CustomerLogoType:
    fileFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelOptionsType:
    customerLogos: typing.Optional[typing.List[CustomerLogoType]] = jstruct.JList[CustomerLogoType]
    waybillTemplate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OnDemandDeliveryType:
    deliveryOption: typing.Optional[str] = None
    location: typing.Optional[str] = None
    specialInstructions: typing.Optional[str] = None
    gateCode: typing.Optional[int] = None
    whereToLeave: typing.Optional[str] = None
    neighbourName: typing.Optional[str] = None
    neighbourHouseNumber: typing.Optional[int] = None
    authorizerName: typing.Optional[str] = None
    servicePointId: typing.Optional[str] = None
    requestedDeliveryDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ImageOptionType:
    typeCode: typing.Optional[str] = None
    templateName: typing.Optional[str] = None
    isRequested: typing.Optional[bool] = None
    invoiceType: typing.Optional[str] = None
    languageCode: typing.Optional[str] = None
    hideAccountNumber: typing.Optional[bool] = None
    numberOfCopies: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class OutputImagePropertiesType:
    printerDPI: typing.Optional[int] = None
    customerBarcodes: typing.Optional[typing.List[BarcodeType]] = jstruct.JList[BarcodeType]
    customerLogos: typing.Optional[typing.List[CustomerLogoType]] = jstruct.JList[CustomerLogoType]
    encodingFormat: typing.Optional[str] = None
    imageOptions: typing.Optional[typing.List[ImageOptionType]] = jstruct.JList[ImageOptionType]
    splitTransportAndWaybillDocLabels: typing.Optional[bool] = None
    allDocumentsInOneImage: typing.Optional[bool] = None
    splitDocumentsByPages: typing.Optional[bool] = None
    splitInvoiceAndReceipt: typing.Optional[bool] = None
    receiptAndLabelsInOneImage: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class PickupType:
    isRequested: typing.Optional[bool] = None
    closeTime: typing.Optional[str] = None
    location: typing.Optional[str] = None
    pickupDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    pickupRequestorDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]


@attr.s(auto_attribs=True)
class ShipmentNotificationType:
    typeCode: typing.Optional[str] = None
    receiverId: typing.Optional[str] = None
    languageCode: typing.Optional[str] = None
    languageCountryCode: typing.Optional[str] = None
    bespokeMessage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValueAddedServiceType:
    serviceCode: typing.Optional[str] = None
    value: typing.Optional[int] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    plannedShippingDateAndTime: typing.Optional[str] = None
    pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    getRateEstimates: typing.Optional[bool] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    valueAddedServices: typing.Optional[typing.List[ValueAddedServiceType]] = jstruct.JList[ValueAddedServiceType]
    outputImageProperties: typing.Optional[OutputImagePropertiesType] = jstruct.JStruct[OutputImagePropertiesType]
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
    content: typing.Optional[ContentType] = jstruct.JStruct[ContentType]
    documentImages: typing.Optional[typing.List[DocumentImageType]] = jstruct.JList[DocumentImageType]
    onDemandDelivery: typing.Optional[OnDemandDeliveryType] = jstruct.JStruct[OnDemandDeliveryType]
    requestOndemandDeliveryURL: typing.Optional[bool] = None
    shipmentNotification: typing.Optional[typing.List[ShipmentNotificationType]] = jstruct.JList[ShipmentNotificationType]
    labelOptions: typing.Optional[LabelOptionsType] = jstruct.JStruct[LabelOptionsType]
