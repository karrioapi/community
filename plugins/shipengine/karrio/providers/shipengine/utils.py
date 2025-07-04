"""Karrio ShipEngine utilities."""

import karrio.lib as lib
import karrio.core.settings as settings


class Settings(settings.Settings):
    """ShipEngine connection settings."""

    api_key: str
    server_url: str = "https://api.shipengine.com"

    @property
    def carrier_name(self):
        return "shipengine"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.shipengine.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def standard_request_serializer(
    request: lib.Serializable,
) -> dict:
    return lib.to_dict(request.serialize())


def standard_response_serializer(
    response: lib.Deserializable[str],
) -> dict:
    return lib.to_dict(response.deserialize())


class ConnectionConfig(lib.Enum):
    """Carrier specific connection configs"""

    platform_name = lib.OptionEnum("platform_name")
    api_key = lib.OptionEnum("api_key")
    server_url = lib.OptionEnum("server_url")
    carrier_id = lib.OptionEnum("carrier_id")
    service_code = lib.OptionEnum("service_code")
    package_code = lib.OptionEnum("package_code")
    confirmation_type = lib.OptionEnum("confirmation_type")
    label_format = lib.OptionEnum("label_format")
    label_layout = lib.OptionEnum("label_layout")
    display_scheme = lib.OptionEnum("display_scheme")
    dry_ice = lib.OptionEnum("dry_ice", bool)
    dry_ice_weight = lib.OptionEnum("dry_ice_weight")
    saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    non_machinable = lib.OptionEnum("non_machinable", bool)
    contains_alcohol = lib.OptionEnum("contains_alcohol", bool)
    delivered_duty_paid = lib.OptionEnum("delivered_duty_paid", bool)
    bill_to_account = lib.OptionEnum("bill_to_account")
    bill_to_country_code = lib.OptionEnum("bill_to_country_code")
    bill_to_party = lib.OptionEnum("bill_to_party")
    bill_to_postal_code = lib.OptionEnum("bill_to_postal_code")
    freight_class = lib.OptionEnum("freight_class")
    freight_charge = lib.OptionEnum("freight_charge")
    cod_payment_type = lib.OptionEnum("cod_payment_type")
    cod_payment_amount = lib.OptionEnum("cod_payment_amount")
    validate_address = lib.OptionEnum("validate_address")
    rate_id = lib.OptionEnum("rate_id")
    warehouse_id = lib.OptionEnum("warehouse_id")
    reference1 = lib.OptionEnum("reference1")
    reference2 = lib.OptionEnum("reference2")
    reference3 = lib.OptionEnum("reference3")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list) 
