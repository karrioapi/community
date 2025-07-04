"""Karrio ShipEngine client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.shipengine.settings as provider_settings

# IMPLEMENTATION INSTRUCTIONS:
# 1. Import the schema types specific to your carrier API
# 2. Uncomment and adapt the request examples below to work with your carrier API
# 3. Replace the stub responses with actual API calls once you've tested with the example data
# 4. Update URLs, headers, and authentication methods as required by your carrier API


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/rates",
        #     data=request.serialize(),
        #     trace=self.trace_as("xml"),
        #     method="POST",
        #     headers={
        #         "Content-Type": "application/xml",
        #         "Authorization": f"Basic {self.settings.authorization}"
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        response = '<r></r>'

        return lib.Deserializable(response, lib.to_element)
    
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/shipments",
        #     data=request.serialize(),
        #     trace=self.trace_as("xml"),
        #     method="POST",
        #     headers={
        #         "Content-Type": "application/xml",
        #         "Authorization": f"Basic {self.settings.authorization}"
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        response = '<r></r>'

        return lib.Deserializable(response, lib.to_element)
    
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/shipments/cancel",
        #     data=request.serialize(),
        #     trace=self.trace_as("xml"),
        #     method="POST",
        #     headers={
        #         "Content-Type": "application/xml",
        #         "Authorization": f"Basic {self.settings.authorization}"
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        response = '<r></r>'

        return lib.Deserializable(response, lib.to_element)
    
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/tracking",
        #     data=request.serialize(),
        #     trace=self.trace_as("xml"),
        #     method="POST",
        #     headers={
        #         "Content-Type": "application/xml",
        #         "Authorization": f"Basic {self.settings.authorization}"
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        response = '<r></r>'

        return lib.Deserializable(response, lib.to_element)
    