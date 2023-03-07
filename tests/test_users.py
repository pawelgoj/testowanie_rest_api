import pytest
import requests
import json
import logging
from types import ModuleType
import allure

from utils import get_unique_user_data


@pytest.mark.usefixtures("url_reqres_in")
class TestUsers:
    logger = logging.getLogger(__name__)
    headers: dict[str, str] = {
        'Content-Type': 'application/json'
    }

    @allure.title("Get users list")
    def test_get_users_list(self, url_reqres_in: str):

        # Given
        url = url_reqres_in + '/users'

        # When
        response = requests.request(
            "GET", url, headers=self.headers)
        self.logger.info(f'Get User list from {url}')
        response_dic = response.json()

        # Then
        assert response.status_code == 200\
            and response_dic['page'] == 1\
            and response_dic['per_page'] == 6\
            and response_dic['total_pages'] == 2\
            and response_dic['data'][0]['id'] == 1\
            and response_dic['data'][5]['id'] == 6\


    @allure.title("Get page 2 of users")
    def test_get_page_2_list_of_users(self, url_reqres_in: str):

        # Given
        url = url_reqres_in + '/users'
        params = {'page': 2}

        # When
        response = requests.request(
            "GET", url, headers=self.headers, params=params)
        self.logger.info(f'Get User list page 2 from {url}')
        response_dic = response.json()

        # Then
        assert response.status_code == 200\
            and response_dic['page'] == 2\
            and response_dic['per_page'] == 6\
            and response_dic['total_pages'] == 2\
            and response_dic['data'][0]['id'] == 7\
            and response_dic['data'][5]['id'] == 12\


    @allure.title("Get user of qiven id")
    def test_get_user_of_id(self, url_reqres_in: str, id: int = 1):

        # Given
        url = url_reqres_in + f'/users/{id}'
        params = {'page': 2}

        # When
        response = requests.request(
            "GET", url, headers=self.headers, params=params)
        self.logger.info(f'User of id {id} from {url}')
        response_dic = response.json()

        # Then
        assert response.status_code == 200\
            and response_dic['data']['id'] == 1

    @allure.title("Create user")
    @pytest.mark.usefixtures("created_users")
    def test_create_new_user(self, url_reqres_in: str, faker: ModuleType):

        # Given
        url = url_reqres_in + f'/users/'
        new_user_data = get_unique_user_data(faker, self.already_created_users)

        new_user_data_s: str = json.dumps(new_user_data)
        # When
        response = requests.post(
            url, headers=self.headers, data=new_user_data_s)
        self.logger.info(
            f'Create new user: {new_user_data_s} by post on: {url}')
        response_dic = response.json()
        new_user_data.update({'id': response_dic['id']})
        self.already_created_users += [new_user_data]

        if 'id' in response_dic.keys():
            self.created_user_id = response_dic['id']

        # Then
        assert response.status_code == 201\
            and 'id' in response_dic.keys()

    @allure.title("Get created user")
    @pytest.mark.usefixtures("created_users")
    def test_get_created_user(self, url_reqres_in: str, faker: ModuleType):

        # Given
        self.test_create_new_user(url_reqres_in, faker)

        print(url_reqres_in)
        url = url_reqres_in + f'/users/{self.created_user_id}'
        self.logger.info(
            f'Get created user of id: {self.created_user_id} by get on: {url}')
        # When
        response = requests.get(url, headers=self.headers)

        response_dic = response.json()
        # Then
        assert response.status_code == 200\
            and hasattr(response_dic, 'id')

    @allure.title("Delete created user")
    @pytest.mark.usefixtures("created_users")
    def test_delete_created_user(self, url_reqres_in: str, faker: ModuleType):

        # Given
        self.test_create_new_user(url_reqres_in, faker)
        url = url_reqres_in + f'/users/{self.created_user_id}'

        # When
        response = requests.delete(url, headers=self.headers)
        self.logger.info(
            f'Delete created user of id: {self.created_user_id} by delete on: {url}')
        if response.status_code == 204:
            self.already_created_users = [item for item in self.already_created_users
                                          if item.get('id', None) != self.created_user_id]

        # Then
        assert response.status_code == 204

    @allure.title("Update user")
    @pytest.mark.usefixture("created_users")
    def test_put_user(self, url_reqres_in: str, faker: ModuleType):

        # Given
        self.test_create_new_user(url_reqres_in, faker)
        url = url_reqres_in + f'/users/{self.created_user_id}'

        new_user_data = json.dumps({
            "last_name": "Pracowity"
        })

        # When
        response = requests.put(url, headers=self.headers)
        self.logger.info(
            f'Update created user of id: {self.created_user_id} by put on: {url}')
        # Then
        assert response.status_code == 200
