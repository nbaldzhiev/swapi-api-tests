"""This module contains a class abstraction of the /vehicles API endpoint."""
from __future__ import annotations


import allure
from requests import Response

from utils.api.endpoints.common_assertions import CommonEndpointAssertions
from config import environment
from utils.api.session_with_base_url import SessionWithBaseUrl


VEHICLE_OBJECT_PROPERTIES = [
    "name",
    "model",
    "manufacturer",
    "cost_in_credits",
    "length",
    "max_atmosphering_speed",
    "crew",
    "passengers",
    "cargo_capacity",
    "consumables",
    "vehicle_class",
    "pilots",
    "films",
    "created",
    "edited",
    "url",
]


class VehiclesEndpoint(SessionWithBaseUrl):
    """This class implement an abstraction of the /vehicles API endpoint."""

    def __init__(self):
        super().__init__(environment["api_base_url"])
        self.endpoint_path = "vehicles/"

    def get_vehicles(self, deserialize: bool = True, overriden_endpoint: str | None = None) -> Response | dict:
        """Makes a GET requests to the endpoint without any query parameters and returns the response either as a
        Response object or a deserialized dictionary.

        Parameters
        ----------
        deserialize : bool
            Whether to deserialize the Response's body.
        overriden_endpoint : str | None
            If provided, the endpoint would be overriden by the value of this parameter, i.e. "vehicles/?page=2"

        Returns
        -------
        Response | dict
        """
        if overriden_endpoint:
            self.endpoint_path = overriden_endpoint
        resp = self.get(self.endpoint_path)
        resp.raise_for_status()
        if deserialize:
            resp = resp.json()
        return resp

    @property
    def assert_that(self) -> VehiclesEndpointAssertions:
        """Returns an instance of VehiclesEndpointAssertions which serves as an interface for assertions on the
        /vehicles endpoint."""
        return VehiclesEndpointAssertions(self)


class VehiclesEndpointAssertions(CommonEndpointAssertions):
    """This class defines common assertions for the /vehicles endpoint."""

    def __init__(self, endpoint: VehiclesEndpoint):
        super().__init__(endpoint=endpoint)
        self.endpoint = endpoint

    @allure.step("Assert That Vehicle Object Has All Expected Properties")
    def vehicle_object_has_all_expected_properties(self, vehicle_obj: dict):
        """Asserts that the given vehicle object, from an API response, contains all expected properties (keys)."""
        assert all(prop in vehicle_obj for prop in VEHICLE_OBJECT_PROPERTIES), "Some property is missing!"
