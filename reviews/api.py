from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Review
from .schemas import ReviewPublicSchema, ReviewSchema, ReviewUpdateSchema

router = Router(tags=['reviews'])


@router.post(
    '/',
    response={HTTPStatus.CREATED: ReviewPublicSchema},
    summary='Criar review',
)
def create_review(request, review: ReviewSchema):
    new_review = Review.objects.create(**review.dict())

    result = Review.objects.select_related('product').get(id=new_review.id)
    return result


@router.put(
    '/{review_id}',
    response={HTTPStatus.OK: ReviewPublicSchema},
    summary='Atualizar review',
)
def update_review(request, review_id: int, review_update: ReviewUpdateSchema):
    review = get_object_or_404(
        Review.objects.select_related('product'), id=review_id
    )
    update_data = review_update.dict(exclude_unset=True)

    for attr, value in update_data.items():
        setattr(review, attr, value)

    review.save()

    return review


@router.delete(
    '/{review_id}',
    response={HTTPStatus.NO_CONTENT: None},
    summary='Deletar review',
)
def delete_review(request, review_id: int):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
