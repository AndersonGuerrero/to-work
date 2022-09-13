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


def create_vacant(client):
    return client.post(
        f'{settings.API_V1_STR}/vacants/',
        json={
            "vacancy_link": "https://www.test.com",
            "position_name": "Python Dev",
            "company_name": "Test company",
            "salary": 99999,
            "currency": "COP"
            },
    )


def test_create_vacant(client: TestClient, test_db):
    response = create_vacant(client)
    assert response.status_code == HTTPStatus.CREATED


def test_create_vacant_bad_link(client: TestClient, test_db):
    response = client.post(
        f'{settings.API_V1_STR}/vacants/',
        json={
            "vacancy_link": "www.test.com",
            "position_name": "Python Dev",
            "company_name": "Test company",
            "salary": 99999,
            "currency": "COP"
            },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_vacant(client: TestClient, test_db):
    vacant = create_vacant(client).json()
    vacant_id = vacant['id']
    response_put = client.put(
        f'{settings.API_V1_STR}/vacants/{vacant_id}',
        json={
            "currency": "USD"
        },
    )
    assert response_put.json()['currency'] == 'USD'
    assert response_put.status_code == HTTPStatus.OK


def test_delete_vacant(client: TestClient, test_db):
    vacant = create_vacant(client).json()
    response = client.delete(
        f'{settings.API_V1_STR}/vacants/{vacant["id"]}',
    )
    assert response.status_code == HTTPStatus.OK


def test_add_skill_vacant(client: TestClient, test_db):
    skill = create_skill(client).json()
    vacant = create_vacant(client).json()
    response = client.post(
        f'{settings.API_V1_STR}/vacants/{vacant["id"]}/add-skills/',
        json={
            "skill_id": skill['id'],
            "value": 5
        },
    )
    vacant = client.get(
        f'{settings.API_V1_STR}/vacants/{vacant["id"]}'
    ).json()
    assert len(vacant['required_skills']) == 1
    assert response.status_code == HTTPStatus.CREATED


def test_remove_skill_vacant(client: TestClient, test_db):
    skill = create_skill(client).json()
    vacant = create_vacant(client).json()
    client.post(
        f'{settings.API_V1_STR}/vacants/{vacant["id"]}/add-skills/',
        json={
            "skill_id": skill['id'],
            "value": 5
        },
    )
    response = client.delete(
        f'{settings.API_V1_STR}/vacants/{vacant["id"]}/remove-skills/'
        f'?skill_id={skill["id"]}'
    )
    vacant = client.get(
        f'{settings.API_V1_STR}/vacants/{vacant["id"]}'
    ).json()
    assert len(vacant['required_skills']) == 0
    assert response.status_code == HTTPStatus.OK
