import karrio.lib as lib
import karrio.core.units as units


class ConnectionConfig(lib.Enum):
    """DHL Express connection configuration options"""
    shipping_services = lib.OptionEnum("shipping_services")


class PackageType(lib.StrEnum):
    """Carrier specific package types"""
    dhl_express_envelope = "ENVELOPE"
    dhl_express_pak = "PAK"
    dhl_express_tube = "TUBE"
    dhl_express_box = "BOX"
    dhl_express_document = "DOCUMENT"
    dhl_express_non_document = "NON_DOCUMENT"

    """ Unified Package type mapping """
    envelope = dhl_express_envelope
    pak = dhl_express_pak
    tube = dhl_express_tube
    pallet = dhl_express_box
    small_box = dhl_express_box
    medium_box = dhl_express_box
    your_packaging = dhl_express_box


class ShippingService(lib.StrEnum):
    """DHL Express specific services"""

    # DHL Express Services
    dhl_express_worldwide = "EXPRESS_WORLDWIDE"
    dhl_express_9_00 = "EXPRESS_9_00"
    dhl_express_12_00 = "EXPRESS_12_00"
    dhl_express_envelope = "EXPRESS_ENVELOPE"
    dhl_express_easy = "EXPRESS_EASY"
    dhl_economy_select = "ECONOMY_SELECT"
    dhl_express_same_day = "EXPRESS_SAME_DAY"
    dhl_express_documents = "EXPRESS_DOCUMENTS"
    
    # Legacy mapping
    express_worldwide = dhl_express_worldwide
    express_12_00 = dhl_express_12_00
    express_9_00 = dhl_express_9_00
    economy_select = dhl_economy_select


class ShippingOption(lib.Enum):
    """DHL Express specific options"""

    pickup_date = lib.OptionEnum("pickup_date")
    pickup_time = lib.OptionEnum("pickup_time")
    delivery_date = lib.OptionEnum("delivery_date")
    delivery_time = lib.OptionEnum("delivery_time")
    declared_value = lib.OptionEnum("declared_value")
    insurance = lib.OptionEnum("insurance")
    signature_required = lib.OptionEnum("signature_required")
    saturday_delivery = lib.OptionEnum("saturday_delivery")
    duties_payment = lib.OptionEnum("duties_payment")
    paperless_trade = lib.OptionEnum("paperless_trade")


class TrackingStatus(lib.Enum):
    on_hold = ["on_hold", "HOLD"]
    delivered = ["delivered", "DELIVERED", "OK"]
    in_transit = ["in_transit", "TRANSIT", "PU", "pickup", "PICKED_UP"]
    delivery_delayed = ["delivery_delayed", "DELAYED"]
    delivery_failed = ["delivery_failed", "FAILED"]
    exception = ["exception", "EXCEPTION"]
    

def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Initialize shipping options for DHL Express.
    """

    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)
