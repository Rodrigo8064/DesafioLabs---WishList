import pytest


@pytest.mark.django_db
def test_user_can_create_users(api_client):
    response = api_client.post(
        '/users/',
        json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
        },
    )

    assert response.status_code == 201
    user_data = response.json()
    assert user_data['username'] == 'newuser'
    assert user_data['email'] == 'newuser@example.com'
    assert user_data['id'] == 1
    assert 'created_at' in user_data
    assert 'updated_at' in user_data


@pytest.mark.django_db
def test_user_update_user(api_client, user, auth_headers):
    response = api_client.put(
        f'/users/{user.id}',
        json={
            'username': 'updateduser',
            'email': 'test@example.com',
            'password': 'secret123',
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    user_data = response.json()
    assert user_data['username'] == 'updateduser'
    assert user_data['email'] == user.email


@pytest.mark.django_db
def test_user_delete_user(api_client, user, auth_headers):
    response = api_client.delete(
        f'/users/{user.id}',
        headers=auth_headers,
    )
    assert response.status_code == 204
