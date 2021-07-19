import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="http://ya.ru",
        help="This is request url"
    )

    parser.addoption(
        "--status_code",
        default=200,
        help="method to execute"
    )


@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")


@pytest.fixture
def url(request):
    return request.config.getoption("--url")
