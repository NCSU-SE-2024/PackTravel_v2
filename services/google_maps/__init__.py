from .routes import Routes


class MapsService:
    """
    A service class for interacting with routing services.

    Attributes:
        routes_service (Routes): An instance of the Routes class to handle route requests.
    """
    routes_service: Routes = None

    def __init__(self, routes_hostname: str, api_key: str):
        """
        Initializes the MapsService class with the specified routing service hostname and API key.

        Args:
            routes_hostname (str): The hostname of the routing service API.
            api_key (str): The API key for authentication with the routing service.
        """
        self.routes_service = Routes(routes_hostname, api_key)

    def get_route_details(self, slat: str, slong: str, dlat: str, dlong: str):
        """
        Retrieves route details including distance and fuel consumption between two geographic locations.

        Args:
            slat (str): The latitude of the starting location.
            slong (str): The longitude of the starting location.
            dlat (str): The latitude of the destination location.
            dlong (str): The longitude of the destination location.

        Returns:
            dict: A dictionary containing the distance in kilometers and fuel consumption in liters,
                  or {'distance': 0, 'fuel': 0} in case of an error or if no route is found.
        """
        return self.routes_service.__get_route_details__(slat, slong, dlat, dlong)
