"""
This module provides classes for managing sensitive configuration settings 
and URL-related configurations by loading them from environment variables.

Classes:
    Secrets: Handles secret keys and sensitive settings such as API keys,
             database connection URLs, and cloud credentials.
    URLConfig: Manages configurations related to hostnames and URLs.
"""

from dotenv import load_dotenv
import os

class Secrets:
    """
    A class to manage secret keys and sensitive configuration settings
    loaded from environment variables.

    Attributes:
        GoogleMapsAPIKey (str): API key for Google Maps services.
        MongoConnectionURL (str): Connection URL for MongoDB.
        CloudCredentials (str): Path to Google Cloud credentials file.
        CloudStorageBucket (str): Name of the Google Cloud Storage bucket.
    """

    GoogleMapsAPIKey = ""
    MongoConnectionURL = ""
    CloudCredentials = "credentials.json"
    CloudStorageBucket = ""

    def __init__(self):
        """
        Initializes the Secrets class and loads environment variables
        to set the class attributes.
        """
        load_dotenv()
        self.MongoConnectionURL = os.getenv("MONGO_CONNECTION_URL")
        self.GoogleMapsAPIKey = os.getenv("GOOGLE_MAPS_API_KEY")
        self.CloudCredentials = os.getenv('GOOGLE_CLOUD_CREDENTIALS')
        self.CloudStorageBucket = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET')


class URLConfig:
    """
    A class to manage configuration settings related to URLs.

    Attributes:
        RoutesHostname (str): Hostname for route-related services.
    """

    RoutesHostname = ""

    def __init__(self):
        """
        Initializes the URLConfig class and loads environment variables
        to set the class attributes.
        """
        load_dotenv()
        self.RoutesHostname = os.getenv("ROUTES_HOSTNAME")
