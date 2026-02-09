from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import File, Form, Query, Router, UploadedFile
from ninja.pagination import paginate, PageNumberPagination

from .models import Product
from .schemas import (
    ProductFilterSchema,
    ProductPublicSchema,
    ProductSchema,
    ProductUpdateSchema,
)

router = Router(tags=['products'])


@router.post(
    '/',
    response={HTTPStatus.CREATED: ProductPublicSchema},
    summary='Criar Produtos',
)
def create_product(
    request, product: Form[ProductSchema], file: File[UploadedFile] = None
):
    new_product = Product.objects.create(
        **product.dict(),
    )
    if file:
        new_product.image.save(file.name, file, save=True)

    return new_product


@router.get(
    '/',
    response={HTTPStatus.OK: List[ProductPublicSchema]},
    summary='Listar produtos',
)
@paginate(PageNumberPagination)
def list_products(
    request,
    filters: ProductFilterSchema = Query(None),
):
    queryset = Product.objects.prefetch_related('reviews').all()

    if filters:
        queryset = filters.filter(queryset)

    return queryset


@router.get(
    '/{product_id}',
    response={HTTPStatus.OK: ProductPublicSchema},
    summary='Buscar produto por ID',
)
def get_product(request, product_id: int):
    product = get_object_or_404(
        Product.objects.prefetch_related('reviews'), id=product_id
    )

    return product


@router.put(
    '/{product_id}',
    response={HTTPStatus.OK: ProductPublicSchema},
    summary='Atualizar produto',
)
def update_product(
    request,
    product_id: int,
    product_update: Form[ProductUpdateSchema],
    file: File[UploadedFile] = None,
):
    product = get_object_or_404(
        Product.objects.prefetch_related('reviews'), id=product_id
    )

    update_data = product_update.dict(exclude_unset=True)

    for attr, value in update_data.items():
        setattr(product, attr, value)

    if file:
        product.image.save(file.name, file, save=False)

    product.save()

    return product


@router.delete(
    '/{product_id}',
    response={HTTPStatus.NO_CONTENT: None},
    summary='Deletar produto',
)
def delete_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    product.delete()
