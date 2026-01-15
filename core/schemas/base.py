from typing import Generic, TypeVar, Optional, Union
from pydantic import BaseModel
from typing_extensions import Literal
from core.domain.errors import ErrorCode

T = TypeVar("T")


class ApiError(BaseModel):
    code: ErrorCode  # e.g., "CARD.NOT_FOUND"
    message: str


class ApiSuccess(Generic[T], BaseModel):
    success: Literal[True]
    data: T


class ApiFailure(BaseModel):
    success: Literal[False]
    error: ApiError


ApiResponse = Union[ApiSuccess[T], ApiFailure]
