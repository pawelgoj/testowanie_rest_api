import pytest
import json


@pytest.fixture()
def get_resources(request) -> dict:
    with open('default_resources.json', 'r') as file:
        request.cls.data = json.load(file)

    yield

    with open("default_resources.json", "w") as file:
        json.dump(request.cls.data, file)


@pytest.fixture()
def url_reqres_in(request) -> str:
    return "https://reqres.in/api"


# To generate parametrization from file
def pytest_generate_tests(metafunc):
    if "user" in metafunc.fixturenames:

        with open("users_in_database_for_tests.json", "r") as file:
            data = file.read()

        users = json.loads(data)
        metafunc.parametrize("user", users)


@pytest.fixture()
def created_users(request):
    """Loads crated users and save created user in test to file 
    (created means in this set of tests that there was an attempt to create a particular user)
    """
    try:
        with open("created-user.json", "r") as file:
            request.cls.already_created_users = json.load(file)
    except FileNotFoundError:
        request.cls.already_created_users = []

    yield

    with open("created-user.json", "w") as file:
        json.dump(request.cls.already_created_users, file)


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['pl_PL']


@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return 12345
