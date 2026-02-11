from http import HTTPStatus
from typing import List

from django.db.models import Q
from django.shortcuts import aget_object_or_404
from ninja import Query, Router
from ninja.errors import HttpError
from ninja.pagination import PageNumberPagination, paginate

from .models import User
from .schemas import (
    UserFilterSchema,
    UserPublicSchema,
    UserSchema,
    UserUpdateSchema,
)

router = Router(tags=['users'])


@router.post(
    '/',
    response={HTTPStatus.CREATED: UserPublicSchema},
    summary='Criar novo usuário',
    auth=None,
)
async def create_user(request, user: UserSchema):
    user_exists = await User.objects.filter(
        Q(email=user.email) | Q(username=user.username)
    ).afirst()

    if user_exists:
        if user_exists.email == user.email:
            raise HttpError(HTTPStatus.BAD_REQUEST, 'Email já está em uso')
        if user_exists.username == user.username:
            raise HttpError(HTTPStatus.BAD_REQUEST, 'Username já está em uso')

    user = await User.objects.acreate_user(**user.dict())
    return user


@router.get(
    '/',
    response={200: List[UserPublicSchema]},
    summary='Listar usuários',
)
@paginate(PageNumberPagination)
async def list_users(
    request,
    search: UserFilterSchema = Query(None),
):
    queryset = User.objects.all()
    if search:
        queryset = search.filter(queryset)

    return queryset


@router.get(
    '/{user_id}',
    response={HTTPStatus.OK: UserPublicSchema},
    summary='Buscar usuário por ID',
)
async def get_user(request, user_id: int):
    user = await aget_object_or_404(User, id=user_id)
    return user


@router.put(
    '/{user_id}',
    response={HTTPStatus.OK: UserPublicSchema},
    summary='Atualizar usuário',
)
async def update_user(request, user_id: int, user_update: UserUpdateSchema):
    if request.auth.id != user_id:
        raise HttpError(HTTPStatus.FORBIDDEN, 'Not emough permissions')
    user = await aget_object_or_404(User, id=user_id)

    for attr, value in user_update.dict(exclude_unset=True).items():
        if attr == 'password':
            user.set_password(value)
        else:
            setattr(user, attr, value)

    await user.asave()

    return user


@router.delete(
    '/{user_id}',
    response={HTTPStatus.NO_CONTENT: None},
    summary='Deletar usuário',
)
async def delete_user(request, user_id: int):
    user = await aget_object_or_404(User, id=user_id)
    await user.adelete()
