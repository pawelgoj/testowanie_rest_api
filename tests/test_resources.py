import pytest
import requests
import json
import logging
import allure

@pytest.mark.usefixtures("url_reqres_in")
class TestResources:
    logger = logging.getLogger(__name__)
    headers: dict[str, str] = {
        'Content-Type': 'application/json'
    }

    @allure.title("Get resources list")
    def test_get_resources_list(self, url_reqres_in: str):

        # Given
        url = url_reqres_in + '/unknown'

        # When
        response = requests.request("GET", url, headers=self.headers)

        self.logger.info(f'Get resource list from {url}')
        response_dic = response.json()

        # Then
        assert response.status_code == 200\
            and response_dic['page'] == 1\
            and response_dic['per_page'] == 6\
            and response_dic['total_pages'] == 2\
            and response_dic['data'][0]['id'] == 1\
            and response_dic['data'][5]['id'] == 6\
            and 'pantone_value' in response_dic['data'][0].keys()

    @allure.title("Get page 2 list of resources")
    def test_get_page_2_list_of_resources(self, url_reqres_in: str):

        # Given
        url = url_reqres_in + '/unknown'
        params = {'page': 2}

        # When
        response = requests.request(
            "GET", url, headers=self.headers, params=params)

        self.logger.info(f'Get resource list page 2 from {url}')
        response_dic = response.json()

        # Then
        assert response.status_code == 200\
            and response_dic['page'] == 2\
            and response_dic['per_page'] == 6\
            and response_dic['total_pages'] == 2\
            and response_dic['data'][0]['id'] == 7\
            and response_dic['data'][5]['id'] == 12\
            and 'pantone_value' in response_dic['data'][0].keys()

    @allure.title("Get resource od given id")
    @pytest.mark.usefixtures("get_resources")
    def test_get_resource_of_id(self, url_reqres_in: str):

        # Given
        id = self.data[0]['id']
        url = url_reqres_in + f'/unknown/{id}'

        # When
        response = requests.request("GET", url, headers=self.headers)

        self.logger.info(f'Resource of id: {id} from {url}')
        response_dic = response.json()

        # Then
        assert response.status_code == 200\
            and response_dic['data']['id'] == id

    @allure.title("Delete resource")
    @pytest.mark.usefixtures("get_resources")
    def test_delete_resource(self, url_reqres_in: str):

        # Given
        id = self.data[0]['id']
        url = url_reqres_in + f'/unknown/{id}'

        # When
        response = requests.delete(url, headers=self.headers)

        self.logger.info(
            f'Delete resource of id: {id} by delete on: {url}')

        if response.status_code == 204:
            self.data.pop(0)

        # Then
        assert response.status_code == 204

    @allure.title("Update resource")
    @pytest.mark.usefixtures("get_resources")
    def test_put_resource(self, url_reqres_in: str):

        # Given
        id = self.data[0]['id']
        url = url_reqres_in + f'/unknown/{id}'

        body_s = json.dumps({
            "year": 2020
        })

        # When
        response = requests.put(url, headers=self.headers, data=body_s)

        self.logger.info(
            f'Update resource of id: {id} by delete on: {url}')

        # Then
        assert response.status_code == 200


@pytest.mark.usefixtures("url_reqres_in")
class TestBenchmark:
    logger = logging.getLogger(__name__)
    headers: dict[str, str] = {
        'Content-Type': 'application/json'
    }
    def test_benchmark(self, url_reqres_in, benchmark):

        @benchmark
        def response():
            # Given
            url = url_reqres_in + '/unknown'

            # When
            response = requests.request("GET", url, headers=self.headers)
            self.logger.info(f'Get resource list from {url}')