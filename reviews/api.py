from http import HTTPStatus

from django.shortcuts import aget_object_or_404
from ninja import Router

from .models import Review
from .schemas import ReviewPublicSchema, ReviewSchema, ReviewUpdateSchema

router = Router(tags=['reviews'])


@router.post(
    '/',
    response={HTTPStatus.CREATED: ReviewPublicSchema},
    summary='Criar review',
)
async def create_review(request, review: ReviewSchema):
    new_review = await Review.objects.acreate(**review.dict())

    result = await Review.objects.select_related('product').aget(id=new_review.id)
    return result


@router.put(
    '/{review_id}',
    response={HTTPStatus.OK: ReviewPublicSchema},
    summary='Atualizar review',
)
async def update_review(request, review_id: int, review_update: ReviewUpdateSchema):
    review = await aget_object_or_404(
        Review.objects.select_related('product'), id=review_id
    )
    update_data = review_update.dict(exclude_unset=True)

    for attr, value in update_data.items():
        setattr(review, attr, value)

    await review.asave()

    return review


@router.delete(
    '/{review_id}',
    response={HTTPStatus.NO_CONTENT: None},
    summary='Deletar review',
)
async def delete_review(request, review_id: int):
    review = await aget_object_or_404(Review, id=review_id)
    await review.adelete()
