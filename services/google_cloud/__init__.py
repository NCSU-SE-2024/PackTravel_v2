from .cloud_storage import CloudStorage
from .credentials import Credentials

class GoogleCloud:
    """
    A class to manage interactions with Google Cloud services, specifically for file storage.
    
    """
    credentials: Credentials = None
    StorageService: CloudStorage = None
    
    def __init__(self, credentials_path: str = "credentials.json", bucket_path: str = 'ptravel-pfp'):
        """
        Initializes the GoogleCloud class with credentials and storage service.

        Args:
            credentials_path (str): Path to the Google Cloud credentials file (default: 'credentials.json').
            bucket_path (str): Name of the bucket for storing files (default: 'ptravel-pfp').
        """
        self.credentials = Credentials(credentials_path)
        self.StorageService = CloudStorage(self.credentials, '')

    def upload_file(self, file, file_name: str = ""):
        """
        Uploads a file to Google Cloud Storage.

        Args:
            file: The file object to upload.
            file_name (str): The destination name for the file in cloud storage (default: "").

        Returns:
            The result of the upload operation from CloudStorage.
        """
        return self.StorageService.__upload_file__(file, destination_blob_name=file_name)