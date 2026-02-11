from datetime import datetime
from decimal import Decimal
from typing import Annotated, List, Optional

from ninja import FilterLookup, FilterSchema, Schema
from pydantic import ConfigDict, field_validator

from reviews.schemas import ReviewProductSchema


class ProductSchema(Schema):
    title: str
    price: Decimal
    description: Optional[str] = None
    brand: str

    @field_validator('title')
    def model_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Título deve ter pelo menos 2 caracteres')
        return v.strip()

    @field_validator('brand')
    def brand_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Marca deve ter pelo menos 2 caracteres')
        return v.strip()

    @field_validator('price')
    def price_validation(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v


class ProductUpdateSchema(Schema):
    title: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    brand: Optional[str] = None

    @field_validator('title')
    def model_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Título deve ter pelo menos 2 caracteres')
        return v.strip()

    @field_validator('brand')
    def brand_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Marca deve ter pelo menos 2 caracteres')
        return v.strip()

    @field_validator('price')
    def price_validation(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v


class ProductPublicSchema(Schema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: Decimal
    description: Optional[str] = None
    image: Optional[str] = None
    brand: str
    reviews: List[ReviewProductSchema] = []
    average_stars: Optional[float] = None
    created_at: datetime
    update_at: Optional[datetime]

    @staticmethod
    def resolve_image(obj):
        if obj.image:
            try:
                return obj.image.url
            except ValueError:
                return None
        return None

    @staticmethod
    def resolve_average_stars(obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(r.stars for r in reviews) / len(reviews)
        return 0


class ProductFilterSchema(FilterSchema):
    search: Annotated[
        Optional[str], FilterLookup(['title__Icontains', 'brand__icontains'])
    ] = None
    min_price: Annotated[Optional[Decimal], FilterLookup('price__gte')] = None
    max_price: Annotated[Optional[Decimal], FilterLookup('price__lte')] = None
