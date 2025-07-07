
import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """ Carrier specific packaging type """
    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingService(lib.StrEnum):
    """ 
    SendCloud Hub Carrier Services
    Since SendCloud is a multi-carrier aggregator, services are dynamically discovered
    from the /fetch-shipping-options API endpoint. These are base service templates.
    """
    
    # Dynamic multi-carrier service pattern: sendcloud_{carrier}_{product}
    # Examples based on API response structure:
    sendcloud_postnl_standard = "postnl:small"
    sendcloud_postnl_signature = "postnl:small/signature" 
    sendcloud_ups_standard = "ups:standard"
    sendcloud_dhl_express = "dhl:express"
    
    # Hub fallback service
    sendcloud_standard = "sendcloud_standard"


class ShippingOption(lib.Enum):
    """ SendCloud specific shipping options based on API functionalities """
    
    # SendCloud API options
    signature = lib.OptionEnum("signature", bool)
    age_check = lib.OptionEnum("age_check", int)  # 16, 18
    insurance = lib.OptionEnum("insurance", float)
    cash_on_delivery = lib.OptionEnum("cash_on_delivery", float)
    dangerous_goods = lib.OptionEnum("dangerous_goods", bool)
    fragile_goods = lib.OptionEnum("fragile_goods", bool)
    weekend_delivery = lib.OptionEnum("weekend_delivery", bool)
    neighbor_delivery = lib.OptionEnum("neighbor_delivery", bool)
    
    # Unified Option type mapping to SendCloud specific options
    sendcloud_signature = signature
    sendcloud_age_check = age_check
    sendcloud_insurance = insurance
    sendcloud_cod = cash_on_delivery
    sendcloud_dangerous = dangerous_goods
    sendcloud_fragile = fragile_goods
    sendcloud_weekend = weekend_delivery
    sendcloud_neighbor = neighbor_delivery


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
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
    """SendCloud tracking status mapping"""
    on_hold = ["processed", "created", "ready_to_send"]
    delivered = ["delivered"]
    in_transit = ["en_route_to_sorting_center", "at_sorting_center", "departed_facility", "out_for_delivery"]
    delivery_failed = ["delivery_attempt_failed", "exception"]
    delivery_delayed = ["delayed"]
    out_for_delivery = ["out_for_delivery", "ready_for_pickup"]
    ready_for_pickup = ["available_for_pickup"]
