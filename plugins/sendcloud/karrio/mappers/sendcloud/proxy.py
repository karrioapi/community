"""Karrio SendCloud client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.sendcloud.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        response = lib.request(
            url=f"{self.settings.server_url}/fetch-shipping-options",
            data=request.serialize(),
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
            url=f"{self.settings.server_url}/parcels",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        shipment_id = request.ctx.get("shipment_id")
        response = lib.request(
            url=f"{self.settings.server_url}/parcels/{shipment_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        tracking_number = request.ctx.get("tracking_number")
        carrier = request.ctx.get("carrier", "")
        
        # SendCloud tracking endpoint
        url = f"{self.settings.server_url}/tracking/{tracking_number}"
        if carrier:
            url = f"{url}/{carrier}"
            
        response = lib.request(
            url=url,
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickups",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        pickup_id = request.ctx.get("pickup_id")
        response = lib.request(
            url=f"{self.settings.server_url}/pickups/{pickup_id}",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        pickup_id = request.ctx.get("pickup_id")
        response = lib.request(
            url=f"{self.settings.server_url}/pickups/{pickup_id}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    