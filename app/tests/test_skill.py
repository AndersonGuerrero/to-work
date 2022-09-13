from http import HTTPStatus
from pytest import fixture

from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.api.deps import get_db
from app.db.test_session import override_get_db, test_db


@fixture
def client() -> TestClient:
    return TestClient(app)


app.dependency_overrides[get_db] = override_get_db


def create_skill(client, name='Python'):
    return client.post(
        f'{settings.API_V1_STR}/skills/',
        json={
            "name": name
        },
    )


def test_create_skill(client: TestClient, test_db):
    response = create_skill(client)
    assert response.status_code == HTTPStatus.CREATED


def test_create_existing_skill(client: TestClient, test_db):
    create_skill(client)
    response = create_skill(client)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_skill(client: TestClient, test_db):
    create_skill(client)
    response_get = client.get(f'{settings.API_V1_STR}/skills/all/').json()
    skill_id = response_get['results'][0]['id']
    response_put = client.put(
        f'{settings.API_V1_STR}/skills/{skill_id}',
        json={
            "name": "Python3.9"
        },
    )
    assert response_put.status_code == HTTPStatus.OK


def test_delete_skill(client: TestClient, test_db):
    response = create_skill(client)
    response_get = client.get(f'{settings.API_V1_STR}/skills/all/').json()
    skill_id = response_get['results'][0]['id']
    response_put = client.delete(
        f'{settings.API_V1_STR}/skills/{skill_id}',
    )
    assert response_put.status_code == HTTPStatus.OK
