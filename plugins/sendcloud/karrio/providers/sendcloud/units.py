import typing
import karrio.lib as lib
import karrio.core.units as units


class LabelFormat(lib.StrEnum):
    """Carrier specific label format"""

    pdf = "pdf"
    png = "png"
    zpl = "zpl"

    PDF = pdf
    PNG = png
    ZPL = zpl


class WeightUnit(lib.StrEnum):
    """Carrier specific weight unit"""

    KG = "kg"
    G = "g"


class DimensionUnit(lib.StrEnum):
    """Carrier specific dimension unit"""

    CM = "cm"
    MM = "mm"


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    PACKAGE = "parcel"
    ENVELOPE = "envelope"
    LETTER = "letter"

    """ Unified Packaging type mapping """
    envelope = ENVELOPE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    sendcloud_service_point_id = lib.OptionEnum("service_point_id")
    sendcloud_insured_value = lib.OptionEnum("insured_value", float)
    sendcloud_contents = lib.OptionEnum("contents")
    sendcloud_require_signature = lib.OptionEnum("require_signature", bool)
    sendcloud_reference = lib.OptionEnum("reference")
    sendcloud_customs_invoice_nr = lib.OptionEnum("customs_invoice_nr")
    sendcloud_customs_shipment_type = lib.OptionEnum("customs_shipment_type")
    sendcloud_order_number = lib.OptionEnum("order_number")
    sendcloud_sender_address_id = lib.OptionEnum("sender_address_id")
    sendcloud_brand_id = lib.OptionEnum("brand_id")


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions=None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["announced"]
    delivered = ["delivered"]
    in_transit = ["in_transit", "ready_to_be_shipped", "being_sorted", "out_for_delivery"]
    delivery_failed = ["delivery_failed", "unable_to_deliver", "no_show"]
    delivery_delayed = []
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_to_be_collected"]


class ShippingService(lib.StrEnum):
    """Sendcloud shipping services"""

    sendcloud_standard = "Standard"
    sendcloud_express = "Express"
    sendcloud_one_day = "One Day"
    sendcloud_same_day = "Same Day"
