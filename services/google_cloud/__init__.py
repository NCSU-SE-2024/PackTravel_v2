"""
GoogleCloud class for managing interactions with Google Cloud services, focusing on file storage.

This class provides functionality to interact with Google Cloud Storage, using credentials and a specified storage service. It allows file uploads to a defined Google Cloud bucket.

Attributes:
    credentials (Credentials): The credentials used for authenticating with Google Cloud services.
    StorageService (CloudStorage): The service used for managing cloud storage interactions, such as uploading files.

Methods:
    __init__(credentials_path: str, bucket_path: str): Initializes the GoogleCloud class with the provided credentials and storage service.
    upload_file(file, file_name: str): Uploads a file to Google Cloud Storage with the specified file name.
"""

from .cloud_storage import CloudStorage
from .credentials import Credentials


class GoogleCloud:
    """
    A class to manage interactions with Google Cloud services, specifically for file storage.

    """

    credentials: Credentials = None
    StorageService: CloudStorage = None

    def __init__(
        self,
        credentials_path: str = "credentials.json",
        bucket_path: str = "ptravelv2-pfp",
    ):
        """
        Initializes the GoogleCloud class with credentials and storage service.

        """
        self.credentials = Credentials(credentials_path)
        self.StorageService = CloudStorage(self.credentials, "")

    def upload_file(self, file, file_name: str = ""):
        """
        Uploads a file to Google Cloud Storage.

        Args:
            file: The file object to upload.
            file_name (str): The destination name for the file in cloud storage (default: "").

        Returns:
            The result of the upload operation from CloudStorage.
        """
        return self.StorageService.__upload_file__(
            file, destination_blob_name=file_name
        )
