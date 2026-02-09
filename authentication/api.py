from django.contrib.auth import authenticate
from ninja import Router

from .auth import create_jwt_token
from .schema import (
    ErrorSchema,
    LoginSchema,
    Token,
)

router = Router(tags=['auth'])


@router.post(
    '/login',
    response={200: Token, 401: ErrorSchema},
    auth=None,
    summary='Gerar token de acesso',
)
def create_token(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)

    if user is None:
        return 401, {'error': 'Invalid email or password'}

    access_token = create_jwt_token(user.id)

    return 200, {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/check')
def check_auth(request):
    return {'authenticated': True, 'user': request.auth.username}
