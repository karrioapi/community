import karrio.schemas.dhl_ecommerce_americas.error as dhl_error
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_americas.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    
    # Handle different error response formats
    errors = []
    
    if isinstance(response, dict):
        # Standard DHL error format with header/body
        if "header" in response and response["header"].get("code", 200) != 200:
            header = response["header"]
            errors.append(models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(header.get("code", "ERROR")),
                message=header.get("message", "Unknown error"),
                details={"messageDetail": header.get("messageDetail", "")},
            ))
        
        # Body-level errors
        if "body" in response and "errors" in response["body"]:
            error_details = response["body"]["errors"]
            for error_item in error_details:
                if isinstance(error_item, dict):
                    error_obj = lib.to_object(dhl_error.ErrorDetail, error_item)
                else:
                    error_obj = error_item
                    
                errors.append(models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error_obj.errorCode or "ERROR",
                    message=error_obj.errorMessage or "Unknown error",
                    details={"description": error_obj.errorDescription or ""},
                ))
        
        # Direct error format
        if "errors" in response:
            error_details = response["errors"]
            for error_item in error_details:
                if isinstance(error_item, dict):
                    error_obj = lib.to_object(dhl_error.ErrorDetail, error_item)
                else:
                    error_obj = error_item
                    
                errors.append(models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error_obj.errorCode or "ERROR",
                    message=error_obj.errorMessage or "Unknown error",
                    details={"description": error_obj.errorDescription or ""},
                ))
        
        # Simple error format
        if "error" in response:
            error_info = response["error"]
            if isinstance(error_info, str):
                errors.append(models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="ERROR",
                    message=error_info,
                ))
            elif isinstance(error_info, dict):
                errors.append(models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error_info.get("code", "ERROR"),
                    message=error_info.get("message", "Unknown error"),
                    details=error_info,
                ))

    return errors
