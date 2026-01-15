import uuid
from typing import Literal, Union

from pydantic import BaseModel

from core.schemas.base import ApiResponse


class CardDraft(BaseModel):
    state: Literal["DRAFT"]
    id: uuid.UUID
    name: str  # 필수만 존재


class CardComplete(BaseModel):
    state: Literal["COMPLETE"]
    id: uuid.UUID
    name: str
    email: str  # 여기선 Optional이 아님!
    phone: str
    image_url: str


CardData = Union[CardDraft, CardComplete]

CardApiResponse = ApiResponse[CardData]
