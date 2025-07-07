from attr import define, field
from typing import Optional, List


@define
class ErrorDetail:
    code: Optional[str] = None
    message: Optional[str] = None
    field: Optional[str] = None


@define
class ErrorResponse:
    errors: Optional[List[ErrorDetail]] = None
    message: Optional[str] = None
    status_code: Optional[int] = None 
