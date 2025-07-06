
import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """ShipEngine packaging types."""
    package = "package"
    letter = "letter"
    thick_envelope = "thick_envelope"

    # Unified mapping
    envelope = letter
    pak = thick_envelope
    small_box = package
    medium_box = package
    large_box = package
    your_packaging = package
    BOX = package  # Add BOX mapping


class ShippingService(lib.StrEnum):
    """Dynamic services discovered from ShipEngine carriers."""

    # Base hub service
    shipengine_auto = "ShipEngine Auto-Select"

    # Common services that will be discovered dynamically
    usps_ground_advantage = "USPS Ground Advantage"
    usps_priority_mail = "USPS Priority Mail"
    usps_priority_mail_express = "USPS Priority Mail Express"
    fedex_ground = "FedEx Ground"
    fedex_2day = "FedEx 2Day"
    fedex_standard_overnight = "FedEx Standard Overnight"
    ups_ground = "UPS Ground"
    ups_3_day_select = "UPS 3 Day Select"
    ups_2nd_day_air = "UPS 2nd Day Air"
    ups_next_day_air = "UPS Next Day Air"
    
    # Test services for ShipEngine integration
    shipengine_ups_ups_ground = "UPS Ground via ShipEngine"

    @classmethod
    def discover_from_rates(cls, rates_response: dict) -> dict:
        """Extract available services from rate response."""
        services = {}

        for rate in rates_response.get("rates", []):
            carrier_code = rate.get("carrier_code", "")
            service_code = rate.get("service_code", "")
            service_name = rate.get("service_type", "")

            # Create dynamic service key only if both carrier_code and service_code exist
            if carrier_code and service_code:
                service_key = f"shipengine_{carrier_code}_{service_code}"
                if service_key not in services:
                    services[service_key] = service_name or service_code

        return services

    @classmethod
    def update_from_response(cls, rates_response: dict):
        """Dynamically add discovered services to enum."""
        discovered = cls.discover_from_rates(rates_response)

        for key, value in discovered.items():
            if not hasattr(cls, key):
                setattr(cls, key, value)


class ShippingOption(lib.Enum):
    """ShipEngine shipping options."""
    # Insurance options
    insurance_amount = lib.OptionEnum("insurance_amount", float)

    # Confirmation options
    delivery_confirmation = lib.OptionEnum("delivery_confirmation", str)
    signature_confirmation = lib.OptionEnum("signature_confirmation", str)
    adult_signature = lib.OptionEnum("adult_signature", bool)

    # Delivery options
    saturday_delivery = lib.OptionEnum("saturday_delivery", bool)

    # Special services
    collect_on_delivery = lib.OptionEnum("collect_on_delivery", float)

    # Unified mappings
    insurance = insurance_amount
    signature_required = signature_confirmation
    cod = collect_on_delivery


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
    """Map ShipEngine tracking statuses to Karrio unified statuses."""
    on_hold = ["on_hold", "returned_to_sender"]
    delivered = ["delivered"]
    in_transit = ["in_transit", "out_for_delivery", "picked_up"]
    delivery_failed = ["delivery_failed", "delivery_attempt_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]


# Weight and dimension units
class WeightUnit(lib.Enum):
    KG = "kilogram"
    LB = "pound"
    OZ = "ounce"
    G = "gram"


class DimensionUnit(lib.Enum):
    CM = "centimeter"
    IN = "inch"
