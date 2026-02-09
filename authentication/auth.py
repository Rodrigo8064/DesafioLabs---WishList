import typing
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import jwt
from django.conf import settings
from ninja.errors import HttpError
from ninja.security import HttpBearer

from users.models import User


def create_jwt_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.now(tz=timezone.utc)
        + timedelta(days=int(settings.JWT_EXPIRATION_MINUTES)),
    }
    return jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def decode_jwt_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HttpError(
            status_code=HTTPStatus.UNAUTHORIZED,
            message='Token has expired',
        )
    except jwt.InvalidTokenError:
        raise HttpError(
            status_code=HTTPStatus.UNAUTHORIZED,
            message='Could not validate credentials',
        )


class BearerAuth(HttpBearer):
    @typing.override
    def authenticate(self, request, token: str):
        payload = decode_jwt_token(token)
        if not payload:
            return None

        try:
            user = User.objects.get(id=payload['user_id'])
            return user
        except User.DoesNotExist:
            return None


jwt_bearer_auth = BearerAuth()
