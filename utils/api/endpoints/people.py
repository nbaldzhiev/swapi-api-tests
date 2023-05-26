"""This module contains a class abstraction of the /people API endpoint."""
from __future__ import annotations

import allure
from requests import Response

from utils.api.endpoints.common_assertions import CommonEndpointAssertions
from config import environment
from utils.api.session_with_base_url import SessionWithBaseUrl


PEOPLE_OBJECT_PROPERTIES = [
    "name",
    "height",
    "mass",
    "hair_color",
    "skin_color",
    "eye_color",
    "birth_year",
    "gender",
    "homeworld",
    "films",
    "species",
    "vehicles",
    "starships",
    "created",
    "edited",
    "url",
]


class PeopleEndpoint(SessionWithBaseUrl):
    """This class implement an abstraction of the People API endpoint."""

    def __init__(self):
        super().__init__(environment["api_base_url"])
        self.endpoint_path = "people/"

    def get_people(self, deserialize: bool = True, overriden_endpoint: str | None = None) -> Response | dict:
        """Makes a GET requests to the endpoint without any query parameters and returns the response either as a
        Response object or a deserialized dictionary.

        Parameters
        ----------
        deserialize : bool
            Whether to deserialize the Response's body.
        overriden_endpoint : str | None
            If provided, the endpoint would be overriden by the value of this parameter, i.e. "people/?page=2"

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
    def assert_that(self) -> PeopleEndpointAssertions:
        """Returns an instance of PeopleEndpointAssertions which serves as an interface for assertions on the
        /people endpoint."""
        return PeopleEndpointAssertions(self)


class PeopleEndpointAssertions(CommonEndpointAssertions):
    """This class defines common assertions for the /people endpoint."""

    def __init__(self, endpoint: PeopleEndpoint):
        super().__init__(endpoint=endpoint)
        self.endpoint = endpoint

    @allure.step("Assert People Object Has All Expected Properties")
    def people_object_has_all_expected_properties(self, people_obj: dict):
        """Asserts that the given people object, from an API response, contains all expected properties (keys)."""
        assert all(prop in people_obj for prop in PEOPLE_OBJECT_PROPERTIES), "Some property is missing!"
