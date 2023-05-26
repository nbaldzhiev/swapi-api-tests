"""This module contains miscellaneous API tests for the app under test."""
from http import HTTPStatus

import allure
import pytest

from utils.api.app_api import AppAPI

pytestmark = allure.parent_suite("API")
from config import environment


@allure.suite("Miscellaneous")
class TestMiscellaneous:
    @allure.title("Querying the base URL")
    def test_query_base_url(self, fixture_app_api: AppAPI):
        """Verifies that querying the base URL, i.e. without a specified endpoint, works as expected."""
        # the PeopleEndpoint instance here is used simply to get access to the requests module's get method
        body = fixture_app_api.people_endpoint.get(environment["api_base_url"]).json()
        assert body == {
            "people": "https://swapi.dev/api/people/",
            "planets": "https://swapi.dev/api/planets/",
            "films": "https://swapi.dev/api/films/",
            "species": "https://swapi.dev/api/species/",
            "vehicles": "https://swapi.dev/api/vehicles/",
            "starships": "https://swapi.dev/api/starships/",
        }, "Incorrect response body!"

    @allure.title("Querying for incorrect endpoint paths")
    @pytest.mark.parametrize(
        "endpoint_path",
        [
            pytest.param("pople", id="incorrect /people path"),
            pytest.param("panets", id="incorrect /planets path"),
            pytest.param("flms", id="incorrect /films path"),
            pytest.param("secies", id="incorrect /species path"),
            pytest.param("vhicles", id="incorrect /vehicles path"),
            pytest.param("sarships", id="incorrect /starships path"),
        ],
    )
    def test_query_incorrect_endpoint_paths(self, fixture_app_api: AppAPI, endpoint_path):
        """Verifies that querying for incorrect endpoint paths causes the SWAPI to return correct status codes."""
        # the PeopleEndpoint instance here is used simply to get access to the requests module's get method
        assert (
            fixture_app_api.people_endpoint.get(environment["api_base_url"] + endpoint_path).status_code
            == HTTPStatus.NOT_FOUND
        ), "Incorrect response status code!"
