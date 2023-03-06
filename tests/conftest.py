import pytest

@pytest.fixture()
def url_reqres_in(request) -> str:
    return "https://reqres.in/api"