"""This module contains a class abstraction of the /planets API endpoint."""
from __future__ import annotations

import allure
from requests import Response

from utils.api.endpoints.common_assertions import CommonEndpointAssertions
from config import environment
from utils.api.session_with_base_url import SessionWithBaseUrl


PLANET_OBJECT_PROPERTIES = [
    "name",
    "rotation_period",
    "orbital_period",
    "diameter",
    "climate",
    "gravity",
    "terrain",
    "surface_water",
    "population",
    "residents",
    "films",
    "created",
    "edited",
    "url",
]


class PlanetsEndpoint(SessionWithBaseUrl):
    """This class implement an abstraction of the Planets API endpoint."""

    def __init__(self):
        super().__init__(environment["api_base_url"])
        self.endpoint_path = "planets/"

    def get_planets(self, deserialize: bool = True, overriden_endpoint: str | None = None) -> Response | dict:
        """Makes a GET requests to the endpoint without any query parameters and returns the response either as a
        Response object or a deserialized dictionary.

        Parameters
        ----------
        deserialize : bool
            Whether to deserialize the Response's body.
        overriden_endpoint : str | None
            If provided, the endpoint would be overriden by the value of this parameter, i.e. "planets/?page=2"

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
    def assert_that(self) -> PlanetsEndpointAssertions:
        """Returns an instance of PeopleEndpointAssertions which serves as an interface for assertions on the
        /planets endpoint."""
        return PlanetsEndpointAssertions(self)


class PlanetsEndpointAssertions(CommonEndpointAssertions):
    """This class defines common assertions for the /planets endpoint."""

    def __init__(self, endpoint: PlanetsEndpoint):
        super().__init__(endpoint=endpoint)
        self.endpoint = endpoint

    @allure.step("Assert That Planet Object Has All Expected Properties")
    def planet_object_has_all_expected_properties(self, planet_obj: dict):
        """Asserts that the given planet object, from an API response, contains all expected properties (keys)."""
        assert all(prop in planet_obj for prop in PLANET_OBJECT_PROPERTIES), "Some property is missing!"
