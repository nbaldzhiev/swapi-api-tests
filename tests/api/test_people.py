"""This module contains API tests for the /people endpoint."""
import re

import allure
import pytest

from utils.api.app_api import AppAPI

pytestmark = allure.parent_suite("API")


@allure.suite("/people Endpoint")
class TestPeopleEndpoint:
    @allure.title("Querying for People without search filters")
    def test_query_people_without_search_params(self, fixture_app_api: AppAPI):
        """Verifies that querying the /people endpoint without providing any search filters works as expected."""

        resp = fixture_app_api.people_endpoint.get_people()
        finished = False
        while not finished:
            for obj in resp["results"]:
                fixture_app_api.people_endpoint.assert_that.people_object_has_all_expected_properties(obj)
            fixture_app_api.people_endpoint.assert_that.resp_has_correct_count_value(resp=resp, expected_value=82)

            if not resp["next"]:
                assert "?page=8" in resp["previous"], "The last page is not the expected one!"
                finished = True
            else:
                resp = fixture_app_api.people_endpoint.get_people(
                    overriden_endpoint=re.match(r".*api/(people/\?page=[1-9])$", resp["next"]).groups()[0]
                )

    @allure.title("Querying for People with search parameters")
    @pytest.mark.parametrize(
        "search_string, names",
        [
            pytest.param("search=Luke", ["Luke Skywalker"], id="one matching result"),
            pytest.param("search=Luke+Skywalker", ["Luke Skywalker"], id="one matching result"),
            pytest.param("search=Darth", ["Darth Vader", "Darth Maul"], id="two matching results"),
            pytest.param("search=Helloworld", [], id="zero matching results"),
        ],
    )
    def test_query_people_with_search_params(self, fixture_app_api: AppAPI, search_string: str, names: list):
        """Verifies that querying the /people endpoint with search filters works as expected."""
        resp = fixture_app_api.people_endpoint.get_people(overriden_endpoint=f"people/?{search_string}")
        resp_names = [obj["name"] for obj in resp["results"]]
        assert all(name in resp_names for name in names), 'Incorrect "name" value of some of the response objects!'
        fixture_app_api.people_endpoint.assert_that.resp_has_correct_count_value(resp=resp, expected_value=len(names))

        for obj in resp["results"]:
            fixture_app_api.people_endpoint.assert_that.people_object_has_all_expected_properties(obj)

            # Verify the response when querying the endpoint URL that is contained as the value of the "url" property
            url_prop_resp = fixture_app_api.people_endpoint.get_people(
                overriden_endpoint=re.match(r".*api/(people/[0-9]+/)$", obj["url"]).groups()[0]
            )
            fixture_app_api.people_endpoint.assert_that.people_object_has_all_expected_properties(url_prop_resp)
            fixture_app_api.people_endpoint.assert_that.object_has_correct_name_value(
                obj=url_prop_resp, expected_value=obj["name"]
            )
