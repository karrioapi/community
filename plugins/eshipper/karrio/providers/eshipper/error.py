import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.eshipper.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        *[{**_, "level": _get_level(_)} for _ in responses if _.get("code")],
        *sum(
            [
                [dict(code="warning", message=__, level="warning") for __ in _.get("warnings")]
                for _ in responses
                if _.get("warnings")
            ],
            [],
        ),
        *sum(
            [
                [
                    dict(
                        code="error",
                        message=order["message"],
                        level="error",
                    )
                    for order in _.get("order", [])
                    if "message" in order and order["message"].startswith("Error")
                ]
                for _ in responses
            ],
            [],
        )
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            level=error.get("level"),
            details={
                **kwargs,
                "type": error.get("type"),
                "fieldErrors": error.get("fieldErrors"),
                "thirdPartyMessage": error.get("thirdPartyMessage"),
            },
        )
        for error in errors
    ]


def _get_level(error: dict) -> str:
    """Determine level from eshipper error response.

    Uses the 'title' field if available (e.g., "Warn"), otherwise defaults to "error".
    """
    title = error.get("title", "").lower()

    if title == "warn" or title == "warning":
        return "warning"
    elif title == "info" or title == "notice":
        return "info"

    return "error"
