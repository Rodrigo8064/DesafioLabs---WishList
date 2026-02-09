from ninja import Schema
from pydantic import ConfigDict

from products.schemas import ProductPublicSchema


class FavoriteSchema(Schema):
    product_id: int


class FavoritePublicSchema(Schema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product: ProductPublicSchema
