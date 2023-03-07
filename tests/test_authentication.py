from types import ModuleType
import allure
import pytest
import requests
import json
import logging
from utils import get_unique_user_email_password



@pytest.mark.usefixtures("url_reqres_in")
class TestAuthentication:
    logger = logging.getLogger(__name__)
    headers: dict[str, str] = {
        'Content-Type': 'application/json'
    }

    @allure.title("Register new user")
    @pytest.mark.usefixtures("created_users")
    def test_register_new_user(self, url_reqres_in: str, faker: ModuleType):

        # Given
        self.logger.info('Get unique eamil and password of user')
        user = get_unique_user_email_password(faker, self.already_created_users)

        url = url_reqres_in + '/register'
        user_s: str = json.dumps(user)

        # When
        self.logger.info(f'POST on {url}')
        response = requests.request(
            "POST", url, headers=self.headers, data=user_s)

        response_dict = response.json()

        if 'id' in response_dict.keys():
            user.update({"id": response_dict['id']})

        self.already_created_users += [user]
        self.new_user_data = user

        # Then
        assert response.status_code == 200\
            and 'id' in response_dict.keys()\
            and 'token' in response_dict.keys()

    @allure.title("Login user")
    @pytest.mark.usefixtures("user")
    def test_login_user(self, url_reqres_in: str, user: dict):
        """Users in mark parametrize are present in database be default"""
        # Given
        user_s: str = json.dumps(user)

        url = url_reqres_in + '/login'

        # When
        self.logger.info(f'Login user: {user_s} on {url}')
        response = requests.request(
            "POST", url, headers=self.headers, data=user_s)

        response_body = response.json()['token']

        self.headers.update({'Authorization': f'Bearer {response_body}'})
        # Then
        assert response.status_code == 200\
            and 'token' in response.json().keys()

    @allure.title("Logout user")
    @pytest.mark.usefixtures("user")
    def test_user_logout(self, url_reqres_in: str, user: dict):
        # preconditions
        self.test_login_user(url_reqres_in, user)

        # Given
        url = url_reqres_in + '/logout'

        # When
        token = self.headers['Authorization']
        self.logger.info(f'Logout user of token: {token} on {url}')
        response = requests.request(
            "POST", url, headers=self.headers
        )

        # Then
        assert response.status_code == 200
