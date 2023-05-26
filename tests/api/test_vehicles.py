"""This module contains API tests for the /vehicles endpoint."""
import re

import allure
import pytest

from utils.api.app_api import AppAPI

pytestmark = allure.parent_suite("API")


@allure.suite("/vehicles Endpoint")
class TestsVehiclesEndpoint:
    @allure.title("Querying for Vehicles without search filters")
    def test_query_vehicles_without_search_params(self, fixture_app_api: AppAPI):
        """Verifies that querying the /vehicles endpoint without providing any search filters works as expected."""
        resp = fixture_app_api.vehicles_endpoint.get_vehicles()

        finished = False
        while not finished:
            for obj in resp["results"]:
                fixture_app_api.vehicles_endpoint.assert_that.vehicle_object_has_all_expected_properties(obj)
            fixture_app_api.vehicles_endpoint.assert_that.resp_has_correct_count_value(resp=resp, expected_value=39)

            if not resp["next"]:
                assert "?page=3" in resp["previous"], "The last page is not the expected one!"
                finished = True
            else:
                resp = fixture_app_api.vehicles_endpoint.get_vehicles(
                    overriden_endpoint=re.match(r".*api/(vehicles/\?page=[1-6])$", resp["next"]).groups()[0]
                )

    @allure.title("Querying for Vehicles with search parameters")
    @pytest.mark.parametrize(
        "search_string, names",
        [
            pytest.param("search=TIE/LN+starfighter", ["TIE/LN starfighter"], id="one matching result by name"),
            pytest.param("search=t-47+airspeeder", ["Snowspeeder"], id="one matching result by model"),
            pytest.param(
                "search=airspeeder",
                ["Snowspeeder", "Koro-2 Exodrive airspeeder", "XJ-6 airspeeder"],
                id="three matching results by name and model",
            ),
            pytest.param("search=Helloworld", [], id="zero matching results"),
        ],
    )
    def test_query_vehicles_with_search_params(self, fixture_app_api: AppAPI, search_string: str, names: list):
        """Verifies that querying the /vehicles endpoint with search filters works as expected."""
        resp = fixture_app_api.vehicles_endpoint.get_vehicles(overriden_endpoint=f"vehicles/?{search_string}")
        resp_names = [obj["name"] for obj in resp["results"]]
        assert all(name in resp_names for name in names), 'Incorrect "name" value of some of the response objects!'
        fixture_app_api.vehicles_endpoint.assert_that.resp_has_correct_count_value(resp=resp, expected_value=len(names))

        for obj in resp["results"]:
            fixture_app_api.vehicles_endpoint.assert_that.vehicle_object_has_all_expected_properties(obj)

            # Verify the response when querying the endpoint URL that is contained as the value of the "url" property
            url_prop_resp = fixture_app_api.vehicles_endpoint.get_vehicles(
                overriden_endpoint=re.match(r".*api/(vehicles/[0-9]+/)$", obj["url"]).groups()[0]
            )
            fixture_app_api.vehicles_endpoint.assert_that.vehicle_object_has_all_expected_properties(url_prop_resp)
            fixture_app_api.vehicles_endpoint.assert_that.object_has_correct_name_value(
                obj=url_prop_resp, expected_value=obj["name"]
            )
