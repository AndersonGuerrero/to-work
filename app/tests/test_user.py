from http import HTTPStatus
from pytest import fixture

from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.api.deps import get_db
from app.db.test_session import override_get_db, test_db
from .test_skill import create_skill


@fixture
def client() -> TestClient:
    return TestClient(app)


app.dependency_overrides[get_db] = override_get_db


def create_user(client):
    return client.post(
        f'{settings.API_V1_STR}/users/',
        json={
            "first_name": "Test first name",
            "last_name": "test last name",
            "email": "test@gmail.com",
            "years_previous_experience": 3
        },
    )


def test_create_user(client: TestClient, test_db):
    response = create_user(client)
    assert response.status_code == HTTPStatus.CREATED


def test_create_user_bad_email(client: TestClient, test_db):
    response = client.post(
        f'{settings.API_V1_STR}/users/',
        json={
            "first_name": "Test first name",
            "last_name": "test last name",
            "email": "test.com",
            "years_previous_experience": 3
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_existing_user(client: TestClient, test_db):
    create_user(client)
    response = create_user(client)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user(client: TestClient, test_db):
    create_user(client)
    response_get = client.get(
        f'{settings.API_V1_STR}/users/search/?max_results=10'
    ).json()
    user_id = response_get['results'][0]['id']
    response_put = client.put(
        f'{settings.API_V1_STR}/users/{user_id}',
        json={
            "name": "Python3.9"
        },
    )
    assert response_put.status_code == HTTPStatus.OK


def test_delete_user(client: TestClient, test_db):
    create_user(client)
    response_get = client.get(
        f'{settings.API_V1_STR}/users/search/?max_results=10'
    ).json()
    user_id = response_get['results'][0]['id']
    response_put = client.delete(
        f'{settings.API_V1_STR}/users/{user_id}',
    )
    assert response_put.status_code == HTTPStatus.OK


def test_add_skill_user(client: TestClient, test_db):
    skill = create_skill(client).json()
    user = create_user(client).json()
    response = client.post(
        f'{settings.API_V1_STR}/users/{user["id"]}/add-skills/',
        json={
            "skill_id": skill['id'],
            "value": 5
        },
    )
    user = client.get(
        f'{settings.API_V1_STR}/users/{user["id"]}'
    ).json()
    assert len(user['skills']) == 1
    assert response.status_code == HTTPStatus.CREATED


def test_remove_skill_user(client: TestClient, test_db):
    skill = create_skill(client).json()
    user = create_user(client).json()
    client.post(
        f'{settings.API_V1_STR}/users/{user["id"]}/add-skills/',
        json={
            "skill_id": skill['id'],
            "value": 5
        },
    )
    response = client.delete(
        f'{settings.API_V1_STR}/users/{user["id"]}/remove-skills/'
        f'?skill_id={skill["id"]}'
    )
    user = client.get(
        f'{settings.API_V1_STR}/users/{user["id"]}'
    ).json()
    assert len(user['skills']) == 0
    assert response.status_code == HTTPStatus.OK
