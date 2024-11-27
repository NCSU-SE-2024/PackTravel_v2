"""
Credentials class to manage Google Cloud service account credentials.

This class is used to handle the authentication process by loading the credentials from a service account file, allowing interactions with Google Cloud services.

Attributes:
    credentials (google.oauth2.service_account.Credentials): The loaded service account credentials used for authenticating requests to Google Cloud services.

Methods:
    __init__(credentials_path: str): Initializes the Credentials class by loading the credentials from the specified service account file.
"""

from google.oauth2 import service_account


class Credentials:
    """
    This class contains credentials logic
    """

    credentials = None

    def __init__(self, credentials_path: str):
        """
        Initializes the Credentials class by loading the credentials from the specified service account file.

        Args:
            credentials_path (str): The path to the service account JSON file containing the credentials.

        """
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
