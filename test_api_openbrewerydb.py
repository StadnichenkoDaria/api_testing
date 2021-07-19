import requests
import pytest


@pytest.fixture(scope="session")
def base_url():
    return "https://"


def test_get_check_status_code_equals_200(base_url):
    response = requests.get(base_url + "www.openbrewerydb.org")
    assert response.status_code == 200


def test_get_check_content_type(base_url):
    response = requests.get(base_url + "www.openbrewerydb.org")
    assert response.headers["Content-Type"] == "text/html; charset=UTF-8"


def test_get_check_query(base_url):
    response = requests.get(base_url + "api.openbrewerydb.org/breweries/search?query=bee")
    response_body = response.json()
    assert response_body[0]["obdb_id"] == "bee-s-knees-ale-house-versailles"


@pytest.mark.parametrize('page', ['1', '2', '10', '100'])
def test_pages(base_url, page):
    response = requests.get(base_url + "api.openbrewerydb.org/breweries?page=" + page)
    assert response.status_code == 200


@pytest.mark.parametrize('per_page', ['0', '1', '10', '50'])
def test_pages(base_url, per_page):
    response = requests.get(base_url + "api.openbrewerydb.org/breweries?per_page=" + per_page)
    response_body = response.json()
    assert len(response_body) == int(per_page)


@pytest.mark.parametrize('per_page', ['51', '100', '1000'])
def test_pages_more_50(base_url, per_page):
    response = requests.get(base_url + "api.openbrewerydb.org/breweries?per_page=" + per_page)
    response_body = response.json()
    assert len(response_body) == 50


@pytest.mark.parametrize('per_page', ['-1', '-100', 'fdg'])
def test_pages_less_20(base_url, per_page):
    response = requests.get(base_url + "api.openbrewerydb.org/breweries?per_page=" + per_page)
    response_body = response.json()
    assert len(response_body) == 20
