"""SendCloud error response schema."""

import attr
from typing import Optional


@attr.s(auto_attribs=True)
class ErrorType:
    code: Optional[int] = None
    message: Optional[str] = None
    request: Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    error: Optional[ErrorType] = None 
