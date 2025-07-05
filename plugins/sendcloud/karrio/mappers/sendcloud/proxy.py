"""Karrio SendCloud client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.sendcloud.utils as provider_utils
import karrio.mappers.sendcloud.settings as provider_settings

# IMPLEMENTATION INSTRUCTIONS:
# 1. Import the schema types specific to your carrier API
# 2. Uncomment and adapt the request examples below to work with your carrier API
# 3. Replace the stub responses with actual API calls once you've tested with the example data
# 4. Update URLs, headers, and authentication methods as required by your carrier API


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        response = lib.request(
            url=f"{self.settings.api_url}/parcels",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.default_response_deserializer,
            on_error=lambda b: provider_utils.default_response_deserializer(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)
    
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        response = lib.request(
            url=f"{self.settings.api_url}/parcels",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.default_response_deserializer,
            on_error=lambda b: provider_utils.default_response_deserializer(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        parcel_id = request.ctx.get("parcel_id") or request.serialize()
        response = lib.request(
            url=f"{self.settings.api_url}/parcels/{parcel_id}",
            data="",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.default_response_deserializer,
            on_error=lambda b: provider_utils.default_response_deserializer(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)
    
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        tracking_number = request.serialize().get("tracking_number")
        response = lib.request(
            url=f"{self.settings.api_url}/parcels",
            data="",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            params={"tracking_number": tracking_number},
            decoder=provider_utils.default_response_deserializer,
            on_error=lambda b: provider_utils.default_response_deserializer(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)
    
