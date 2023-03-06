import pytest
import requests
import json
import logging


@pytest.mark.usefixtures("url_reqres_in")
class TestAuthentication:

    new_user_data: str = json.dumps({
        "email": "george.bluth@reqres.in",
        "password": "superPassword"
    })

    headers: dict[str, str] = {
        'Content-Type': 'application/json'
    }

    def test_register_new_user(self, url_reqres_in: str):

        # Given

        url = url_reqres_in + '/register'

        # When
        response = requests.request(
            "POST", url, headers=self.headers, data=self.new_user_data)

        # Then
        assert response.status_code == 200\
            and 'id' in response.json().keys()\
            and 'token' in response.json().keys()

    def test_login_new_user(self, url_reqres_in: str):

        # Given

        url = url_reqres_in + '/login'

        # When
        response = requests.request(
            "POST", url, headers=self.headers, data=self.new_user_data)

        self.headers.update({'Authorization': 'Bearer QpwL5tke4Pnpja7X1'})
        # Then
        assert response.status_code == 200\
            and 'token' in response.json().keys()

    def test_user_logout(self, url_reqres_in: str):

        # Given

        url = url_reqres_in + '/logout'

        # When
        response = requests.request(
            "POST", url, headers=self.headers, data=self.new_user_data
        )

        # Then
        assert response.status_code == 200
