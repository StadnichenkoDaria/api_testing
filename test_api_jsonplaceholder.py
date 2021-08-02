import requests
import cerberus
import pytest


@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"


def test_get_check_status_code_equals_200(base_url):
    response = requests.get(base_url)
    assert response.status_code == 200


def test_api_json_schema(base_url):
    res = requests.get(base_url + "/todos/1")

    schema = {
        "userId": {"type": "number"},
        "id": {"type": "number"},
        "title": {"type": "string"},
        "completed": {"type": "boolean"},
    }
    v = cerberus.Validator()
    assert v.validate(res.json(), schema)


def test_api_post_request(base_url):
    res = requests.post(
        base_url + "/posts",
        data={'userId': 11, 'id': 101, 'title': 'test title', 'body': 'test body'})
    res_json = res.json()
    assert res_json['userId'] == '11'
    assert res_json['id'] == 101
    assert res_json['title'] == 'test title'
    assert res_json['body'] == 'test body'


@pytest.mark.parametrize('id', ['1', '20', '100'])
def test_id_get(base_url, id):
    response = requests.get(base_url + "/todos/" + id)
    response_body = response.json()
    assert response_body["id"] == int(id)


@pytest.mark.parametrize('id', ['1', '30', '110'])
def test_id_delete(base_url, id):
    response = requests.delete(base_url + "/posts/" + id)
    response_body = response.json()
    assert len(response_body) == 0
