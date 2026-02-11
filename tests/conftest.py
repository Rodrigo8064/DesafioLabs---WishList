import pytest
from ninja.testing import TestClient

from app.api import api
from authentication.auth import create_jwt_token
from users.models import User


@pytest.fixture(scope='session')
def api_client():
    api_client = TestClient(api)
    return api_client


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        username='test_driver',
        email='test@example.com',
        password='password123',
    )

    return user


@pytest.fixture
def auth_headers(user):
    token = create_jwt_token(user.id)
    return {"Authorization": f"Bearer {token}"}
