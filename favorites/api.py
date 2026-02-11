from http import HTTPStatus
from typing import List

from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import PageNumberPagination, paginate

from products.models import Product

from .models import Favorite
from .schemas import FavoritePublicSchema, FavoriteSchema

router = Router(tags=['favorites'])


@router.post(
    '/',
    response={HTTPStatus.CREATED: FavoritePublicSchema},
    summary='Favoritar produto',
)
async def add_favorite_product(request, product: FavoriteSchema):
    if not await Product.objects.filter(id=product.product_id).aexists():
        raise HttpError(HTTPStatus.NOT_FOUND, 'Produto não encontrado')

    user = request.auth

    favorite, created = await Favorite.objects.aget_or_create(
        user=user, product_id=product.product_id
    )

    if not created:
        raise HttpError(
            HTTPStatus.BAD_REQUEST, 'Você já favoritou este produto'
        )

    return await Favorite.objects.select_related('product').aget(id=favorite.id)


@router.get(
    '/',
    response={HTTPStatus.OK: List[FavoritePublicSchema]},
    summary='Listar produtos favoritados',
)
@paginate(PageNumberPagination)
async def list_favorite(
    request,
):
    queryset = Favorite.objects.select_related('product').filter(
        user=request.auth
    )

    return queryset


@router.delete(
    '/{product_id}',
    response={HTTPStatus.NO_CONTENT: None},
    summary='Deletar Produto Favoritado',
)
async def delete_favorite_product(request, product_id: int):
    product = await aget_object_or_404(
        Favorite, product_id=product_id, user=request.auth
    )
    await product.adelete()
