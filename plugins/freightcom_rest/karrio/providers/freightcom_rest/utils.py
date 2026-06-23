
import base64
import datetime
import typing

import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors

import math

class Settings(core.Settings):
    """Freightcom Rest connection settings."""

    # Add carrier specific api connection properties here
    api_key: str

    @property
    def carrier_name(self):
        return "freightcom_rest"

    @property
    def server_url(self):
        return (
            "https://customer-external-api.ssd-test.freightcom.com"
            if self.test_mode
            else "https://external-api.freightcom.com"
        )


    # """uncomment the following code block to expose a carrier tracking url."""
    # @property
    # def tracking_url(self):
    #     return "https://www.carrier.com/tracking?tracking-id={}"

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def payment_method(self):

        if not self.connection_config.payment_method_type.state:
            raise Exception(f"Payment method type not set")
        cache_key = f"payment|{self.carrier_name}|{self.connection_config.payment_method_type.state}|{self.api_key}"

        payment = self.connection_cache.get(cache_key) or {}
        payment_id = payment.get("id")

        if payment_id:
            return payment_id

        self.connection_cache.set(cache_key, lambda: get_payment_id(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth.get("id")

    @property
    def customs_and_duties_payment_method(self):

        if not self.connection_config.customs_and_duties_payment_method.state:
            raise Exception(f"Customs and duties payment method type not set")
        cache_key = f"payment|{self.carrier_name}|{self.connection_config.customs_and_duties_payment_method.state}|{self.api_key}"

        payment = self.connection_cache.get(cache_key) or {}
        payment_id = payment.get("id")

        if payment_id:
            return payment_id

        self.connection_cache.set(cache_key, lambda: get_customs_payment_id(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth.get("id")


def download_document_to_base64(file_url: str) -> str:
    return lib.request(
        decoder=lambda b: base64.encodebytes(b).decode("utf-8"),
        url=file_url,
    )


def ceil(value: typing.Optional[float]) -> typing.Optional[int]:
    if value is None:
        return None
    return math.ceil(value)


def is_usmca_eligible(shipper_country: str, recipient_country: str) -> bool:
    """Check if shipment is eligible for USMCA customs handling (US, CA, MX)."""
    USMCA_COUNTRIES = {"US", "CA", "MX"}
    return (
        (shipper_country in USMCA_COUNTRIES and recipient_country in USMCA_COUNTRIES) and
        shipper_country != recipient_country
    )

def get_payment_id(settings: Settings) -> dict:

    try:
        from karrio.mappers.freightcom_rest.proxy import Proxy

        proxy = Proxy(settings)
        response = proxy._get_payments_methods()
        methods = response.deserialize()

        selected_method = next((
            method for method in methods
            if settings.connection_config.payment_method_type.type.map(
            method.get('type')).name == settings.connection_config.payment_method_type.state
        ), None)


        if not selected_method:
            raise Exception(f"Payment method {settings.connection_config.payment_method_type.state} not found in API")

        return selected_method

    except Exception as e:
        raise

def get_customs_payment_id(settings: Settings) -> dict:

    try:
        from karrio.mappers.freightcom_rest.proxy import Proxy

        proxy = Proxy(settings)
        response = proxy._get_payments_methods()
        methods = response.deserialize()

        selected_method = next((
            method for method in methods
            if settings.connection_config.customs_and_duties_payment_method.type.map(
            method.get('type')).name == settings.connection_config.customs_and_duties_payment_method.state
        ), None)


        if not selected_method:
            raise Exception(f"Customs payment method {settings.connection_config.customs_and_duties_payment_method.state} not found in API")

        return selected_method

    except Exception as e:
        raise


class PaymentMethodType(lib.StrEnum):
    net_terms = "net-terms"
    credit_card = "credit-card"

class CustomsPaymentMethodType(lib.StrEnum):
    """Payment method type for customs and duties (credit-card only)"""
    credit_card = "credit-card"

class ConnectionConfig(lib.Enum):
    """Carrier specific connection configs"""
    payment_method_type = lib.OptionEnum("payment_method_type", PaymentMethodType)
    customs_and_duties_payment_method = lib.OptionEnum("customs_and_duties_payment_method", CustomsPaymentMethodType)
    request_guaranteed_customs_charges = lib.OptionEnum("request_guaranteed_customs_charges", bool, default=True)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)

