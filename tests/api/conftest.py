"""This module contains fixtures to be used within the API tests."""
import pytest

from utils.api.app_api import AppAPI


@pytest.fixture
def fixture_app_api() -> AppAPI:
    """Function-scoped fixture for obtaining an object of the App under test's API interface."""
    return AppAPI()
