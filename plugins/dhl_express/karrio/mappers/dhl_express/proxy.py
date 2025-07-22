"""Karrio DHL Express client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dhl_express.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        # Handle both list and dict tracking requests
        serialized = request if isinstance(request, list) else request.serialize()
        if isinstance(serialized, list):
            tracking_numbers = serialized
        else:
            tracking_numbers = serialized.get("trackingNumbers", [])
            
        query_param = ",".join(tracking_numbers)
        response = lib.request(
            url=f"{self.settings.server_url}/track/shipments?trackingNumber={query_param}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/shipments",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        request_data = request.serialize()
        if isinstance(request_data, str):
            import json
            request_data = json.loads(request_data)
        shipment_id = request_data.get("shipmentTrackingNumber")
        response = lib.request(
            url=f"{self.settings.server_url}/shipments/{shipment_id}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)
