"""This module contains a class declaration to allow for creating sessions with a base url set."""
from urllib.parse import urljoin

from requests import Session


class SessionWithBaseUrl(Session):
    """This class inherits requests.Session and overwrites the request() method in order to set a base url so that
    the base API url doesn't need to be provided each time a request is made."""
    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)
