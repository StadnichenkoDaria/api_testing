import cerberus
import requests
import pytest


@pytest.fixture(scope="session")
def base_url():
    return "https://dog.ceo/"


def test_get_check_status_code_equals_200(base_url):
    response = requests.get(base_url + "dog-api/documentation/")
    assert response.status_code == 200


def test_api_json_schema(base_url):
    res = requests.get(base_url + "api/breeds/image/random")

    schema = {
        "message": {"type": "string"},
        "status": {"type": "string"}
    }
    v = cerberus.Validator()
    assert v.validate(res.json(), schema)


def test_create_add_get(base_url):
    response = requests.get(base_url + "api/breed/hound")
    assert response.status_code == 404
    assert response.json().get("status") == "error"
    assert response.json().get("message") == "Breed not found (No info file for this breed exists)"


def test_get_check_content_type_equals_json(base_url):
    response = requests.get(base_url + "api/breed/hound/images/random")
    assert response.headers["Content-Type"] == "application/json"


def test_get_len_list(base_url):
    response = requests.get(base_url + "api/breeds/list/all")
    response_body = response.json()
    assert len(response_body["message"]) == 95


@pytest.mark.parametrize('breed', ['african', 'boxer', 'dingo', 'husky'])
def test_breed(base_url, breed):
    response = requests.get(base_url + "api/breed/" + breed + "/images/random")
    response_body = response.json()
    assert response_body["status"] == 'success'


@pytest.mark.parametrize('breed', ['afghan', 'ovcharka', 'appenzeller'])
def test_breed_negative(base_url, breed):
    response = requests.get(base_url + "/api/breeds/list/all/" + breed)
    response_body = response.json()
    assert response_body["code"] == 404
