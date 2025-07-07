import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Veho specific packaging type"""
    PACKAGE = "PACKAGE"

    """Unified Packaging type mapping"""
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingService(lib.StrEnum):
    """Veho specific services"""
    veho_ground_plus = "groundPlus"
    veho_premium_economy = "premiumEconomy"


class ShippingOption(lib.Enum):
    """Veho specific options"""
    delivery_max_datetime = lib.OptionEnum("delivery_max_datetime", str)
    label_date = lib.OptionEnum("label_date", str)

    """Unified Option type mapping"""
    insurance = delivery_max_datetime


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]


def is_ground_plus(service: str) -> bool:
    """Check if the service is Veho Ground Plus"""
    return service == ShippingService.veho_ground_plus


def is_premium_economy(service: str) -> bool:
    """Check if the service is Veho Premium Economy"""
    return service == ShippingService.veho_premium_economy


def get_service_name(service: str) -> str:
    """Get the display name for a service"""
    service_names = {
        ShippingService.veho_ground_plus: "Veho Ground Plus",
        ShippingService.veho_premium_economy: "Veho Premium Economy",
    }
    return service_names.get(service, service)
