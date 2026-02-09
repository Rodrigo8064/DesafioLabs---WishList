from http import HTTPStatus
from typing import List

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Query, Router
from ninja.errors import HttpError
from ninja.security import django_auth_is_staff
from ninja.pagination import paginate, PageNumberPagination

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
def create_user(request, user: UserSchema):
    user_exists = User.objects.filter(
        Q(email=user.email) | Q(username=user.username)
    ).first()

    if user_exists:
        if user_exists.email == user.email:
            raise HttpError(HTTPStatus.BAD_REQUEST, 'Email já está em uso')
        if user_exists.username == user.username:
            raise HttpError(HTTPStatus.BAD_REQUEST, 'Username já está em uso')

    user = User.objects.create_user(**user.dict())
    return user


@router.get(
    '/',
    response={200: List[UserPublicSchema]},
    summary='Listar usuários',
    auth=django_auth_is_staff,
)
@paginate(PageNumberPagination)
def list_users(
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
    auth=django_auth_is_staff,
)
def get_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    return user


@router.put(
    '/{user_id}',
    response={HTTPStatus.OK: UserPublicSchema},
    summary='Atualizar usuário',
)
def update_user(request, user_id: int, user_update: UserUpdateSchema):
    if request.auth.id != user_id:
        raise HttpError(HTTPStatus.FORBIDDEN, 'Not emough permissions')
    user = get_object_or_404(User, id=user_id)

    for attr, value in user_update.dict(exclude_unset=True).items():
        if attr == 'password':
            user.set_password(value)
        else:
            setattr(user, attr, value)

    user.save()

    return user


@router.delete(
    '/{user_id}',
    response={HTTPStatus.NO_CONTENT: None},
    summary='Deletar usuário',
    auth=django_auth_is_staff,
)
def delete_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    user.delete()
