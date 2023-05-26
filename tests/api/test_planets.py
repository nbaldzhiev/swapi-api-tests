"""This module contains API tests for the /planets endpoint."""
import re

import allure
import pytest

from utils.api.app_api import AppAPI

pytestmark = allure.parent_suite("API")


@allure.suite("/planets Endpoint")
class TestPlanetsEndpoint:
    @allure.title("Querying for Planets without search filters")
    def test_query_planets_without_search_params(self, fixture_app_api: AppAPI):
        """Verifies that querying the /planets endpoint without providing any search filters works as expected."""
        resp = fixture_app_api.planets_endpoint.get_planets()

        finished = False
        while not finished:
            for obj in resp["results"]:
                fixture_app_api.planets_endpoint.assert_that.planet_object_has_all_expected_properties(obj)
            fixture_app_api.planets_endpoint.assert_that.resp_has_correct_count_value(resp=resp, expected_value=60)

            if not resp["next"]:
                assert "?page=5" in resp["previous"], "The last page is not the expected one!"
                finished = True
            else:
                resp = fixture_app_api.planets_endpoint.get_planets(
                    overriden_endpoint=re.match(r".*api/(planets/\?page=[1-6])$", resp["next"]).groups()[0]
                )

    @allure.title("Querying for Planets with search parameters")
    @pytest.mark.parametrize(
        "search_string, names",
        [
            pytest.param("search=Concord", ["Concord Dawn"], id="one matching result"),
            pytest.param("search=Concord+Dawn", ["Concord Dawn"], id="one matching result"),
            pytest.param("search=Ch", ["Chandrila", "Iktotch", "Champala"], id="three matching results"),
            pytest.param("search=Helloworld", [], id="zero matching results"),
        ],
    )
    def test_query_planets_with_search_params(self, fixture_app_api: AppAPI, search_string: str, names: list):
        """Verifies that querying the /planets endpoint with search filters works as expected."""
        resp = fixture_app_api.planets_endpoint.get_planets(overriden_endpoint=f"planets/?{search_string}")
        resp_names = [obj["name"] for obj in resp["results"]]
        assert all(name in resp_names for name in names), 'Incorrect "name" value of some of the response objects!'
        fixture_app_api.planets_endpoint.assert_that.resp_has_correct_count_value(resp=resp, expected_value=len(names))

        for obj in resp["results"]:
            fixture_app_api.planets_endpoint.assert_that.planet_object_has_all_expected_properties(obj)

            # Verify the response when querying the endpoint URL that is contained as the value of the "url" property
            url_prop_resp = fixture_app_api.planets_endpoint.get_planets(
                overriden_endpoint=re.match(r".*api/(planets/[0-9]+/)$", obj["url"]).groups()[0]
            )
            fixture_app_api.planets_endpoint.assert_that.planet_object_has_all_expected_properties(url_prop_resp)
            fixture_app_api.planets_endpoint.assert_that.object_has_correct_name_value(
                obj=url_prop_resp, expected_value=obj["name"]
            )
