"""This module contains a class with common assertions for all endpoints."""
from __future__ import annotations

import allure


class CommonEndpointAssertions:
    """This class defines common assertions for all endpoints."""

    def __init__(self, endpoint):
        self.endpoint = endpoint

    @allure.step('Assert That The "count" Property Has A Correct Value')
    def resp_has_correct_count_value(self, resp: dict, expected_value: int):
        """Asserts that a given API response has a correct expected value for the count property."""
        assert resp["count"] == expected_value, 'Incorrect "count" property value!'

    @allure.step('Assert That A Given Object Has Correct "name" Property Value')
    def object_has_correct_name_value(self, obj: dict, expected_value: str):
        """Asserts that a given object has a correct expected value for the name property."""
        assert obj["name"] == expected_value, 'Incorrect "name" property value!'
