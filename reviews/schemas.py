from datetime import datetime
from typing import Optional

from ninja import Schema
from pydantic import ConfigDict, field_validator


class ReviewSchema(Schema):
    product_id: int
    stars: int
    comment: Optional[str] = None

    @field_validator('stars')
    def price_validation(cls, v):
        if v < 0 or v > 5:
            raise ValueError('Estrelas devem estar entre 0 e 5')
        return v


class ReviewUpdateSchema(Schema):
    stars: Optional[int] = None
    comment: Optional[str] = None

    @field_validator('stars')
    def price_validation(cls, v):
        if v < 0 or v > 5:
            raise ValueError('Estrelas devem estar entre 0 e 5')
        return v


class ProductSimpleSchema(Schema):
    id: int
    title: str


class ReviewPublicSchema(Schema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product: ProductSimpleSchema
    stars: int
    comment: Optional[str] = None
    created_at: datetime
