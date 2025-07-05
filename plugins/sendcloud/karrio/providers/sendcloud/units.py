"""Karrio SendCloud shipping units and enumerations."""

import re
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class LabelType(lib.Enum):
    """SendCloud supported label formats."""
    PDF = "PDF"
    PNG = "PNG"
    ZPL = "ZPL"


class PaymentType(lib.StrEnum):
    """SendCloud payment types."""
    sender = "SENDER"
    recipient = "RECIPIENT"
    third_party = "THIRD_PARTY"


class PackagingType(lib.StrEnum):
    """SendCloud packaging types."""
    package = "package"
    envelope = "envelope"
    box = "box"
    tube = "tube"
    pallet = "pallet"
    
    # SendCloud specific packaging types
    sendcloud_box = "box"
    sendcloud_package = "package"
    sendcloud_envelope = "envelope"
    sendcloud_tube = "tube"
    sendcloud_pallet = "pallet"

    # Unified Packaging type mapping
    small_box = package
    medium_box = package
    large_box = package
    your_packaging = package


class ShippingService(lib.StrEnum):
    """SendCloud shipping services."""
    sendcloud_standard = "standard"
    sendcloud_express = "express"
    sendcloud_economy = "economy"
    sendcloud_priority = "priority"
    sendcloud_overnight = "overnight"
    sendcloud_international = "international"
    sendcloud_domestic = "domestic"
    
    # Common service aliases
    standard = sendcloud_standard
    express = sendcloud_express
    economy = sendcloud_economy
    priority = sendcloud_priority
    overnight = sendcloud_overnight


class ShippingOption(lib.Enum):
    """SendCloud shipping options."""
    sendcloud_signature_required = lib.OptionEnum("signature_required", bool)
    sendcloud_insurance = lib.OptionEnum("insurance", float)
    sendcloud_saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    sendcloud_delivery_confirmation = lib.OptionEnum("delivery_confirmation", bool)
    sendcloud_cash_on_delivery = lib.OptionEnum("cash_on_delivery", float)
    sendcloud_hold_for_pickup = lib.OptionEnum("hold_for_pickup", bool)
    sendcloud_adult_signature = lib.OptionEnum("adult_signature", bool)
    sendcloud_reference_number = lib.OptionEnum("reference_number", str)
    sendcloud_delivery_instructions = lib.OptionEnum("delivery_instructions", str)
    sendcloud_packaging_type = lib.OptionEnum("packaging_type", str)
    sendcloud_label_format = lib.OptionEnum("label_format", str)
    sendcloud_currency = lib.OptionEnum("currency", str)
    sendcloud_shipment_date = lib.OptionEnum("shipment_date", str)
    sendcloud_dry_ice = lib.OptionEnum("dry_ice", bool)
    sendcloud_hazmat = lib.OptionEnum("hazmat", bool)
    
    # Unified Option type mapping
    insurance = sendcloud_insurance
    signature_confirmation = sendcloud_signature_required
    saturday_delivery = sendcloud_saturday_delivery
    cash_on_delivery = sendcloud_cash_on_delivery
    hold_for_pickup = sendcloud_hold_for_pickup
    currency = sendcloud_currency
    shipment_date = sendcloud_shipment_date
    delivery_confirmation = sendcloud_delivery_confirmation
    adult_signature = sendcloud_adult_signature
    reference_number = sendcloud_reference_number
    delivery_instructions = sendcloud_delivery_instructions
    packaging_type = sendcloud_packaging_type
    label_format = sendcloud_label_format
    dry_ice = sendcloud_dry_ice
    hazmat = sendcloud_hazmat


class TrackingStatus(lib.Enum):
    """SendCloud tracking status mapping."""
    announced = ["announced", "info_received"]
    in_transit = ["in_transit", "transit", "shipped", "dispatched"]
    out_for_delivery = ["out_for_delivery", "ready_for_delivery"]
    delivery_attempted = ["delivery_attempted", "delivery_failed"]
    delivered = ["delivered", "delivered_to_recipient"]
    exception = ["exception", "error", "problem"]
    return_to_sender = ["return_to_sender", "returning"]
    cancelled = ["cancelled", "canceled"]
    pending = ["pending", "processing"]
    ready_for_pickup = ["ready_for_pickup", "awaiting_pickup"]
    on_hold = ["on_hold", "held"]
    delivery_delayed = ["delivery_delayed", "delayed"]
    
    # Default mappings
    unknown = ["unknown", "other"]


class ConnectionConfig(lib.Enum):
    """SendCloud connection configuration options."""
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, LabelType.PDF.value)
    test_mode = lib.OptionEnum("test_mode", bool, False)
    metadata = lib.OptionEnum("metadata", dict)


def shipping_options_initializer(
    payload: typing.Any,
    package_options: units.ShippingOptions=None,
) -> units.ShippingOptions:
    options = {}
    
    if hasattr(payload, "label_type") and payload.label_type:
        options.update(
            sendcloud_label_format=LabelType.map(payload.label_type or "PDF").value,
        )
    
    if hasattr(payload, "options") and payload.options:
        options.update(payload.options)
    
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


def validate_service(service_code: str) -> bool:
    """
    Validate if a service code is supported by SendCloud.
    
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
        "standard": "SendCloud Standard",
        "express": "SendCloud Express",
        "economy": "SendCloud Economy",
        "priority": "SendCloud Priority",
        "overnight": "SendCloud Overnight",
        "international": "SendCloud International",
        "domestic": "SendCloud Domestic",
    }
    return service_mapping.get(service_code, f"SendCloud {service_code.title()}")


def get_packaging_type(packaging: str) -> str:
    """
    Map unified packaging type to SendCloud specific type.
    
    Args:
        packaging: The packaging type
        
    Returns:
        SendCloud specific packaging type
    """
    return getattr(PackagingType, packaging, PackagingType.package).value
