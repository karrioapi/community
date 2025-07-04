"""Karrio Veho client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.veho.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        shipment_id = request.serialize().get("shipmentIdentifier")
        
        response = lib.request(
            url=f"{self.settings.server_url}/shipments/{shipment_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        request_data = request.serialize()
        tracking_numbers = request_data.get("trackingNumbers", [])
        
        # Make a single request with all tracking numbers
        response = lib.request(
            url=f"{self.settings.server_url}/tracking",
            data=lib.to_json({"trackingNumbers": tracking_numbers}),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
