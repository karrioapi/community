"""Karrio SendCloud client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.sendcloud.utils as provider_utils
import karrio.mappers.sendcloud.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        response = lib.request(
            url=f"{self.settings.server_url}/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        shipment_id = request.serialize().get("shipment_identifier")
        response = lib.request(
            url=f"{self.settings.server_url}/shipments/{shipment_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        tracking_numbers = request.serialize().get("tracking_numbers", [])
        response = lib.request(
            url=f"{self.settings.server_url}/tracking",
            data=lib.to_json({"tracking_numbers": tracking_numbers}),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
