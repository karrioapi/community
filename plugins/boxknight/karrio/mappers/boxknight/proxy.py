"""Karrio BoxKnight client proxy."""

import typing
import base64
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.providers.boxknight.error as provider_error
import karrio.mappers.boxknight.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Retrieve the auth token using the username|password pair
        or collect it from the cache if an unexpired token exist.
        """
        cache_key = f"{self.settings.carrier_name}|{self.settings.username}|{self.settings.password}"

        def get_token():
            result = lib.request(
                url=f"{self.settings.server_url}/soap/services/LoginService/V2_1",
                trace=self.settings.trace_as("json"),
                method="POST",
                data=dict(
                    username=self.settings.username,
                    password=self.settings.password,
                ),
                max_retries=2,
            )

            response = lib.to_dict(result)
            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages=messages)

            return dict(token=response["token"])

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="token",
        )

        return lib.Deserializable(token.get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        auth_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Authorization": auth_token},
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        auth_token = self.authenticate().deserialize()
        payload = request.serialize()
        result = lib.to_dict(
            lib.request(
                url=f"{self.settings.server_url}/orders",
                data=payload["order"],
                trace=self.trace_as("json"),
                method="POST",
                headers={"Authorization": auth_token},
            )
        )

        response = (
            dict(
                order_id=result["id"],
                label_type=payload["label_type"],
                service=payload["order"]["service"],
                label=lib.request(
                    url=f"{self.settings.server_url}/labels/{result['id']}?format={payload['label_type']}",
                    decoder=lambda b: base64.encodebytes(b).decode("utf-8"),
                    headers={"Authorization": auth_token},
                    trace=self.trace_as("json"),
                ),
            )
            if result.get("error") is None
            else result
        )

        return lib.Deserializable(response)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        auth_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/orders/{request.serialize()['order_id']}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={"Authorization": auth_token},
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        auth_token = self.authenticate().deserialize()

        track = lambda data: (
            data["order_id"],
            lib.request(
                url=f"{self.settings.server_url}/orders/{data['order_id']}",
                trace=self.trace_as("json"),
                method="GET",
                headers={"Authorization": auth_token},
            ),
        )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            track, requests.serialize()
        )

        return lib.Deserializable(
            responses,
            lambda response: [(key, lib.to_dict(res)) for key, res in response],
        )
