import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelDownloadType:
    pdf: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    label_id: typing.Optional[str] = None
    shipment_id: typing.Optional[str] = None
    tracking_number: typing.Optional[str] = None
    carrier_id: typing.Optional[str] = None
    carrier_code: typing.Optional[str] = None
    service_code: typing.Optional[str] = None
    label_download: typing.Optional[LabelDownloadType] = jstruct.JStruct[LabelDownloadType]
