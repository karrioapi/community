import typing
import pathlib
import karrio.lib as lib
import karrio.core.units as units


class LabelFormat(lib.StrEnum):
    """Carrier specific label format"""

    pdf = "pdf"
    png = "png"
    zpl = "zpl"
    url = "url"

    PDF = pdf
    PNG = png
    ZPL = zpl


class DimensionUnit(lib.StrEnum):
    """Carrier specific dimension unit"""

    CM = "cm"
    IN = "in"


class WeightUnit(lib.StrEnum):
    """Carrier specific weight unit"""

    LB = "lb"
    KG = "kg"


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    sendcloud_service_point_id = lib.OptionEnum("service_point_id")
    sendcloud_apply_shipping_rules = lib.OptionEnum("apply_shipping_rules", bool)
    sendcloud_request_label = lib.OptionEnum("request_label", bool)
    sendcloud_request_label_async = lib.OptionEnum("request_label_async", bool)
    sendcloud_insured_value = lib.OptionEnum("insured_value", int)
    sendcloud_external_order_id = lib.OptionEnum("external_order_id")
    sendcloud_external_shipment_id = lib.OptionEnum("external_shipment_id")
    sendcloud_customs_invoice_nr = lib.OptionEnum("customs_invoice_nr")
    sendcloud_customs_shipment_type = lib.OptionEnum("customs_shipment_type")
    sendcloud_total_order_value = lib.OptionEnum("total_order_value")
    sendcloud_total_order_value_currency = lib.OptionEnum("total_order_value_currency")
    sendcloud_is_return = lib.OptionEnum("is_return", bool)
    # fmt: on


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
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]


# Basic SendCloud shipping services
ShippingService = lib.StrEnum(
    "ShippingService",
    {
        "sendcloud_standard": "SendCloud Standard",
        "sendcloud_express": "SendCloud Express",
        "sendcloud_morning": "SendCloud Morning",
        "sendcloud_evening": "SendCloud Evening",
        "sendcloud_same_day": "SendCloud Same Day",
        "sendcloud_package_point": "SendCloud Package Point",
        "sendcloud_dpd_pickup": "SendCloud DPD Pickup",
        "sendcloud_dhl_express": "SendCloud DHL Express",
        "sendcloud_ups_standard": "SendCloud UPS Standard",
        "sendcloud_fedex_international": "SendCloud FedEx International",
    },
)

ShippingServiceID = lib.StrEnum(
    "ShippingServiceID",
    {
        "1": "sendcloud_standard",
        "2": "sendcloud_express",
        "3": "sendcloud_morning",
        "4": "sendcloud_evening",
        "5": "sendcloud_same_day",
        "6": "sendcloud_package_point",
        "7": "sendcloud_dpd_pickup",
        "8": "sendcloud_dhl_express",
        "9": "sendcloud_ups_standard",
        "10": "sendcloud_fedex_international",
    },
)

ShippingCourierID = lib.StrEnum(
    "ShippingCourierID",
    {
        "dpd": "DPD",
        "dhl": "DHL",
        "ups": "UPS",
        "fedex": "FedEx",
        "postnl": "PostNL",
        "gls": "GLS",
        "hermes": "Hermes",
        "bpost": "bpost",
        "dhl_express": "DHL Express",
        "ups_express": "UPS Express",
    },
) 
