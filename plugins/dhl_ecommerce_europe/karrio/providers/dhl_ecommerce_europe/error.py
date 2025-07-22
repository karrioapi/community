import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_europe.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses: typing.List[dict] = sum(
        [
            res.get("errors", [])
            for res in (response if isinstance(response, list) else [response])
        ],
        start=[],
    )
    errors = [res for res in responses]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            details={
                **kwargs,
                **(dict(parameters=error.get("parameter")) if error.get("parameter") else {}),
            },
        )
        for error in errors
    ]
