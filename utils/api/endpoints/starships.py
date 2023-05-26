"""This module contains a class abstraction of the /starships API endpoint."""
from __future__ import annotations

import allure
from requests import Response

from utils.api.endpoints.common_assertions import CommonEndpointAssertions
from config import environment
from utils.api.session_with_base_url import SessionWithBaseUrl


STARSHIP_OBJECT_PROPERTIES = [
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
    "hyperdrive_rating",
    "MGLT",
    "starship_class",
    "pilots",
    "films",
    "created",
    "edited",
    "url",
]


class StarshipsEndpoint(SessionWithBaseUrl):
    """This class implement an abstraction of the Planets API endpoint."""

    def __init__(self):
        super().__init__(environment["api_base_url"])
        self.endpoint_path = "starships/"

    def get_starships(self, deserialize: bool = True, overriden_endpoint: str | None = None) -> Response | dict:
        """Makes a GET requests to the endpoint without any query parameters and returns the response either as a
        Response object or a deserialized dictionary.

        Parameters
        ----------
        deserialize : bool
            Whether to deserialize the Response's body.
        overriden_endpoint : str | None
            If provided, the endpoint would be overriden by the value of this parameter, i.e. "starships/?page=2"

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
    def assert_that(self) -> StarshipsEndpointAssertions:
        """Returns an instance of StarhipsEndpointAssertions which serves as an interface for assertions on the
        /starships endpoint."""
        return StarshipsEndpointAssertions(self)


class StarshipsEndpointAssertions(CommonEndpointAssertions):
    """This class defines common assertions for the /starships endpoint."""

    def __init__(self, endpoint: StarshipsEndpoint):
        super().__init__(endpoint=endpoint)
        self.endpoint = endpoint

    @allure.step("Assert That Starship Object Has All Expected Properties")
    def starship_object_has_all_expected_properties(self, starship_obj: dict):
        """Asserts that the given starship object, from an API response, contains all expected properties (keys)."""
        assert all(prop in starship_obj for prop in STARSHIP_OBJECT_PROPERTIES), "Some property is missing!"
