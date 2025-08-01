"""Karrio Sendcloud API proxy."""

import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.sendcloud.utils as provider_utils


class Proxy(proxy.Proxy):
    settings: provider_utils.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/shipping-methods",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Content-Type": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/parcels",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Content-Type": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        payload = request.serialize()
        parcel_id = payload.get("parcel_id")
        
        response = lib.request(
            url=f"{self.settings.server_url}/parcels/{parcel_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Content-Type": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        payload = request.serialize()
        tracking_number = payload.get("tracking_number")
        
        response = lib.request(
            url=f"{self.settings.server_url}/parcels",
            trace=self.trace_as("json"),
            method="GET",
            params={"tracking_number": tracking_number},
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Content-Type": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/label",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Content-Type": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        payload = request.serialize()
        pickup_id = payload.get("pickup_id")
        
        response = lib.request(
            url=f"{self.settings.server_url}/label/{pickup_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Content-Type": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)
