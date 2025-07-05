"""Karrio ShipEngine shipping units and enumerations."""

import re
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class LabelType(lib.Enum):
    """ShipEngine supported label formats."""
    PDF = "PDF"
    PNG = "PNG"
    ZPL = "ZPL"
    EPL2 = "EPL2"


class PaymentType(lib.StrEnum):
    """ShipEngine payment types."""
    sender = "SENDER"
    recipient = "RECIPIENT"
    third_party = "THIRD_PARTY"
    collect = "COLLECT"


class PackagingType(lib.StrEnum):
    """ShipEngine packaging types."""
    package = "package"
    envelope = "envelope"
    box = "box"
    tube = "tube"
    pallet = "pallet"
    
    # ShipEngine specific packaging types
    shipengine_box = "box"
    shipengine_package = "package"
    shipengine_envelope = "envelope"
    shipengine_tube = "tube"
    shipengine_pallet = "pallet"
    shipengine_pak = "pak"
    shipengine_letter = "letter"
    shipengine_flat_rate_envelope = "flat_rate_envelope"
    shipengine_flat_rate_box = "flat_rate_box"
    shipengine_regional_box = "regional_box"

    # Unified Packaging type mapping
    small_box = package
    medium_box = package
    large_box = package
    your_packaging = package
    pak = envelope
    letter = envelope
    flat_rate_envelope = envelope
    flat_rate_box = box
    regional_box = box


class ShippingService(lib.StrEnum):
    """ShipEngine shipping services."""
    shipengine_standard = "standard"
    shipengine_express = "express"
    shipengine_economy = "economy"
    shipengine_priority = "priority"
    shipengine_overnight = "overnight"
    shipengine_ground = "ground"
    shipengine_next_day = "next_day"
    shipengine_two_day = "two_day"
    shipengine_three_day = "three_day"
    shipengine_international = "international"
    shipengine_domestic = "domestic"
    
    # Common service aliases
    standard = shipengine_standard
    express = shipengine_express
    economy = shipengine_economy
    priority = shipengine_priority
    overnight = shipengine_overnight
    ground = shipengine_ground
    next_day = shipengine_next_day
    two_day = shipengine_two_day
    three_day = shipengine_three_day


class ShippingOption(lib.Enum):
    """ShipEngine shipping options."""
    shipengine_signature_required = lib.OptionEnum("signature_required", bool)
    shipengine_insurance = lib.OptionEnum("insurance", float)
    shipengine_saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    shipengine_delivery_confirmation = lib.OptionEnum("delivery_confirmation", bool)
    shipengine_cash_on_delivery = lib.OptionEnum("cash_on_delivery", float)
    shipengine_hold_for_pickup = lib.OptionEnum("hold_for_pickup", bool)
    shipengine_adult_signature = lib.OptionEnum("adult_signature", bool)
    shipengine_reference_number = lib.OptionEnum("reference_number", str)
    shipengine_delivery_instructions = lib.OptionEnum("delivery_instructions", str)
    shipengine_packaging_type = lib.OptionEnum("packaging_type", str)
    shipengine_label_format = lib.OptionEnum("label_format", str)
    shipengine_currency = lib.OptionEnum("currency", str)
    shipengine_shipment_date = lib.OptionEnum("shipment_date", str)
    shipengine_dry_ice = lib.OptionEnum("dry_ice", bool)
    shipengine_hazmat = lib.OptionEnum("hazmat", bool)
    shipengine_residential = lib.OptionEnum("residential", bool)
    shipengine_po_box = lib.OptionEnum("po_box", bool)
    shipengine_return_receipt = lib.OptionEnum("return_receipt", bool)
    shipengine_certified_mail = lib.OptionEnum("certified_mail", bool)
    shipengine_registered_mail = lib.OptionEnum("registered_mail", bool)
    
    # Unified Option type mapping
    insurance = shipengine_insurance
    signature_confirmation = shipengine_signature_required
    saturday_delivery = shipengine_saturday_delivery
    cash_on_delivery = shipengine_cash_on_delivery
    hold_for_pickup = shipengine_hold_for_pickup
    currency = shipengine_currency
    shipment_date = shipengine_shipment_date
    delivery_confirmation = shipengine_delivery_confirmation
    adult_signature = shipengine_adult_signature
    reference_number = shipengine_reference_number
    delivery_instructions = shipengine_delivery_instructions
    packaging_type = shipengine_packaging_type
    label_format = shipengine_label_format
    dry_ice = shipengine_dry_ice
    hazmat = shipengine_hazmat
    residential = shipengine_residential
    po_box = shipengine_po_box
    return_receipt = shipengine_return_receipt
    certified_mail = shipengine_certified_mail
    registered_mail = shipengine_registered_mail


class TrackingStatus(lib.Enum):
    """ShipEngine tracking status mapping."""
    unknown = ["unknown", "not_yet_in_system"]
    pre_transit = ["pre_transit", "label_created"]
    in_transit = ["in_transit", "transit", "shipped", "dispatched"]
    out_for_delivery = ["out_for_delivery", "ready_for_delivery"]
    delivery_attempted = ["delivery_attempted", "delivery_failed"]
    delivered = ["delivered", "delivered_to_recipient"]
    exception = ["exception", "error", "problem"]
    return_to_sender = ["return_to_sender", "returning"]
    cancelled = ["cancelled", "canceled", "voided"]
    pending = ["pending", "processing"]
    ready_for_pickup = ["ready_for_pickup", "awaiting_pickup"]
    on_hold = ["on_hold", "held"]
    delivery_delayed = ["delivery_delayed", "delayed"]
    
    # ShipEngine specific statuses
    accepted = ["accepted", "accepted_by_carrier"]
    in_transit_to_destination = ["in_transit_to_destination"]
    arrived_at_destination = ["arrived_at_destination"]
    departed_from_origin = ["departed_from_origin"]


class ConnectionConfig(lib.Enum):
    """ShipEngine connection configuration options."""
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, LabelType.PDF.value)
    test_mode = lib.OptionEnum("test_mode", bool, False)
    metadata = lib.OptionEnum("metadata", dict)
    warehouse_id = lib.OptionEnum("warehouse_id", str)
    carrier_id = lib.OptionEnum("carrier_id", str)


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions=None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    
    Args:
        options: Dictionary of shipping options
        package_options: Existing package options to merge
        
    Returns:
        Initialized ShippingOptions object
    """
    _options = options or {}
    
    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


def validate_service(service_code: str) -> bool:
    """
    Validate if a service code is supported by ShipEngine.
    
    Args:
        service_code: The service code to validate
        
    Returns:
        True if valid, False otherwise
    """
    return service_code in [service.value for service in ShippingService]


def get_service_name(service_code: str) -> str:
    """
    Get the human-readable name for a service code.
    
    Args:
        service_code: The service code
        
    Returns:
        Human-readable service name
    """
    service_mapping = {
        "standard": "ShipEngine Standard",
        "express": "ShipEngine Express",
        "economy": "ShipEngine Economy",
        "priority": "ShipEngine Priority",
        "overnight": "ShipEngine Overnight",
        "ground": "ShipEngine Ground",
        "next_day": "ShipEngine Next Day",
        "two_day": "ShipEngine Two Day",
        "three_day": "ShipEngine Three Day",
        "international": "ShipEngine International",
        "domestic": "ShipEngine Domestic",
    }
    return service_mapping.get(service_code, f"ShipEngine {service_code.title()}")


def get_packaging_type(packaging: str) -> str:
    """
    Map unified packaging type to ShipEngine specific type.
    
    Args:
        packaging: The packaging type
        
    Returns:
        ShipEngine specific packaging type
    """
    return getattr(PackagingType, packaging, PackagingType.package).value


def format_tracking_number(tracking_number: str) -> str:
    """
    Format tracking number for ShipEngine.
    
    Args:
        tracking_number: The tracking number to format
        
    Returns:
        Formatted tracking number
    """
    # Remove any non-alphanumeric characters
    return re.sub(r'[^a-zA-Z0-9]', '', tracking_number.upper())
