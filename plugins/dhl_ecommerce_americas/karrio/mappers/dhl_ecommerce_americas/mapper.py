"""Karrio DHL eCommerce Americas mapper."""

import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_americas.rate as rate
import karrio.providers.dhl_ecommerce_americas.tracking as tracking
import karrio.providers.dhl_ecommerce_americas.shipment as shipment
import karrio.mappers.dhl_ecommerce_americas.settings as provider_settings


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings

    def create_rate_request(self, payload: models.RateRequest) -> lib.Serializable:
        return rate.rate_request(payload, self.settings)

    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return tracking.tracking_request(payload, self.settings)

    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return shipment.shipment_request(payload, self.settings)

    def create_cancel_shipment_request(
        self, payload: models.ShipmentCancelRequest
    ) -> lib.Serializable:
        return shipment.shipment_cancel_request(payload, self.settings)

    def parse_rate_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
        return rate.parse_rate_response(response, self.settings)

    def parse_tracking_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[
        typing.List[models.TrackingDetails], typing.List[models.Message]
    ]:
        return tracking.parse_tracking_response(response, self.settings)

    def parse_shipment_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return shipment.parse_shipment_response(response, self.settings)

    def parse_cancel_shipment_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return shipment.parse_shipment_cancel_response(response, self.settings)
