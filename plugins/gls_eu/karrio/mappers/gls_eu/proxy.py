import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.gls_eu.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(
        self,
        request: lib.Serializable,
    ) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/backend/rs/shipments",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/glsVersion-3.4+json",
                "Accept": "application/glsVersion-3.4+json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(
        self,
        request: lib.Serializable,
    ) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/backend/rs/shipments",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/glsVersion-3.4+json",
                "Accept": "application/glsVersion-3.4+json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(
        self,
        request: lib.Serializable,
    ) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/backend/rs/tracking",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/glsVersion-3.4+json",
                "Accept": "application/glsVersion-3.4+json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(
        self,
        request: lib.Serializable,
    ) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/backend/rs/collection",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/glsVersion-3.4+json",
                "Accept": "application/glsVersion-3.4+json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict) 