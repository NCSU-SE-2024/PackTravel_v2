from .credentials import Credentials
from google.cloud import storage

class CloudStorage:
    """
    A class to handle file uploads to a Google Cloud Storage bucket.
    """
    credentials: Credentials = None
    PfpBucket: str = ""

    def __init__(self, credentials: Credentials, pfp_bucket: str = ""):
        """
        Initializes the CloudStorage class with specified credentials and bucket name.

        Args:
            credentials (Credentials): Google Cloud credentials for authentication.
            pfp_bucket (str): The name of the Google Cloud Storage bucket (default: "").
        """
        self.credentials = credentials
        self.PfpBucket = pfp_bucket

    def __upload_file__(self, file, destination_blob_name: str) -> str:
        """
        Uploads a file to the specified Google Cloud Storage bucket.

        Args:
            file: The file object to be uploaded.
            destination_blob_name (str): The name of the file as it will appear in the cloud storage.

        Returns:
            str: The public URL of the uploaded file.
        """
        client = storage.Client(credentials=self.credentials.credentials)
        bucket = client.bucket('ptravelv2-pfp')
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(file)
        return blob.public_url  
