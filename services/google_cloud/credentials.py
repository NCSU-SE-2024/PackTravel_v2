from google.oauth2 import service_account


class Credentials:
    credentials = None

    def __init__(self, credentials_path: str):
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path)
