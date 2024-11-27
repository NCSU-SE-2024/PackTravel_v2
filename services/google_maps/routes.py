"""
Routes class for handling routing API requests to compute route details.

This class provides functionality to interact with a routing API, fetching route information, including distance and fuel consumption, between two geographic locations.

Attributes:
    hostname (str): The hostname of the routing API.
    api_key (str): The API key for authentication with the routing API.

Methods:
    __init__(hostname: str, api_key: str): Initializes the Routes class with the specified API hostname and authentication key.
    __get_route_details__(slat: str, slong: str, dlat: str, dlong: str): Fetches route details (distance and fuel consumption) between two locations.
"""

import json
from http import client


class Routes:
    """
    A class to handle routing requests to a specified API.
    """

    hostname = ""
    api_key = ""

    def __init__(self, hostname: str, api_key=""):
        """
        Initializes the Routes class with the hostname and API key.

        Args:
            hostname (str): The hostname of the routing API.
            api_key (str): The API key for authentication (default is an empty string).
        """
        self.hostname = hostname
        self.api_key = api_key

    def __get_route_details__(
            self, slat: str, slong: str, dlat: str, dlong: str):
        """
        Retrieves route details including distance and fuel consumption between two geographic locations.

        Args:
            slat (str): The latitude of the starting location.
            slong (str): The longitude of the starting location.
            dlat (str): The latitude of the destination location.
            dlong (str): The longitude of the destination location.

        Returns:
            dict: A dictionary containing the distance in kilometers and fuel consumption in liters.
                  Returns {'distance': 0, 'fuel': 0} in case of an error or if no route is found.
        """
        try:
            conn = client.HTTPSConnection(self.hostname, timeout=1)
            payload = json.dumps(
                {
                    "origin": {
                        "location": {"latLng": {"latitude": slat, "longitude": slong}}
                    },
                    "destination": {
                        "location": {"latLng": {"latitude": dlat, "longitude": dlong}}
                    },
                    "routeModifiers": {"vehicleInfo": {"emissionType": "GASOLINE"}},
                    "travelMode": "DRIVE",
                    "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
                    "extraComputations": ["FUEL_CONSUMPTION"],
                }
            )

            headers = {
                "content-type": "application/json",
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.routeLabels,routes.routeToken,routes.travelAdvisory.fuelConsumptionMicroliters",
            }
            conn.request(
                "POST",
                "/directions/v2:computeRoutes",
                payload,
                headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            return {
                "distance": int(data.get("routes", [])[0].get("distanceMeters", 0))
                / 1000,
                "fuel": int(
                    data.get("routes", [])[0]
                    .get("travelAdvisory", {})
                    .get("fuelConsumptionMicroliters", 0)
                )
                / (1000 * 1000),
            }
        except BaseException:
            return {
                "distance": 0,
                "fuel": 0,
            }
