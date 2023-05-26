"""This module contains an implementation of an API interface to serve as an interface for using the API of the app
under test."""

from utils.api.endpoints.people import PeopleEndpoint
from utils.api.endpoints.planets import PlanetsEndpoint
from utils.api.endpoints.starships import StarshipsEndpoint
from utils.api.endpoints.vehicles import VehiclesEndpoint


class AppAPI:
    """This class defines the behaviour and serves as an interface for using the API of the app under test."""

    def __init__(self):
        self.people_endpoint: PeopleEndpoint = PeopleEndpoint()
        self.planets_endpoint: PlanetsEndpoint = PlanetsEndpoint()
        self.starships_endpoint: StarshipsEndpoint = StarshipsEndpoint()
        self.vehicles_endpoint: VehiclesEndpoint = VehiclesEndpoint()
