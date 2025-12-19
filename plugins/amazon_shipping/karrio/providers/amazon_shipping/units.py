import karrio.lib as lib


class PackagingType(lib.StrEnum):
    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class Service(lib.StrEnum):
    amazon_shipping_ground = "Amazon Shipping Ground"
    amazon_shipping_standard = "Amazon Shipping Standard"
    amazon_shipping_premium = "Amazon Shipping Premium"


class TrackingStatus(lib.Enum):
    on_hold = []
    delivered = ["Delivered"]
    in_transit = []
    delivery_failed = []
    out_for_delivery = []


class TrackingIncidentReason(lib.Enum):
    """Maps Amazon Shipping exception codes to normalized TrackingIncidentReason."""
    carrier_damaged_parcel = []
    consignee_refused = []
    consignee_not_home = []
    unknown = []
