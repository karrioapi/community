"""Karrio GLS EU mapper implementation."""

import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.gls_eu as provider
import karrio.mappers.gls_eu.settings as provider_settings


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings

    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return provider.tracking_request(payload, self.settings)

    def parse_tracking_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
        return provider.parse_tracking_response(response, self.settings)

    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)

    def parse_shipment_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)

    def create_shipment_cancel_request(
        self, payload: models.ShipmentCancelRequest
    ) -> lib.Serializable:
        return provider.shipment_cancel_request(payload, self.settings)

    def parse_shipment_cancel_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_shipment_cancel_response(response, self.settings)

    def create_pickup_request(
        self, payload: models.PickupRequest
    ) -> lib.Serializable:
        return provider.pickup_request(payload, self.settings)

    def parse_pickup_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return provider.parse_pickup_response(response, self.settings)

    def create_pickup_cancel_request(
        self, payload: models.PickupCancelRequest
    ) -> lib.Serializable:
        return provider.pickup_cancel_request(payload, self.settings)

    def parse_pickup_cancel_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_pickup_cancel_response(response, self.settings)
