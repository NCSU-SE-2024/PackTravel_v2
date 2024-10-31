from django.core.exceptions import ValidationError
from utils import get_client
import re

userDB = None

def intializeDB():
    """
    Initializes the MongoDB client and sets up the `userDB` collection for user data storage.

    This function checks if the global `userDB` variable is uninitialized (i.e., `None`). 
    If so, it retrieves a MongoDB client instance using the `get_client()` function 
    from the `utils` module and accesses the `userData` collection within the 
    `SEProject` database.

    Globals:
        userDB (Collection): The MongoDB collection object for user data storage.

    Returns:
        None
    """
    global userDB
    if(userDB == None):
        client = get_client()
        db = client.SEProject
        userDB = db.userData

def validate_email_domain(value):
    """
    Validates that the provided email address meets specific criteria.

    This function checks that the email:
    - Contains only alphanumeric characters in the local part (before the "@" symbol).
    - Belongs to the allowed domain, "ncsu.edu".
    - Contains exactly one "@" symbol, separating the local part and domain.
    
    Args:
        value (str): The email address to validate.

    Raises:
        ValidationError: If the email format is invalid or if the domain is not "ncsu.edu".
    """
    pattern = re.compile("^[a-zA-Z0-9]+$")
    allowed_domain = 'ncsu.edu'
    email_parts = value.split('@')
    domain = email_parts[-1]
    if len(email_parts) != 2:
        raise ValidationError(f"Invalid email")
    if not pattern.match(email_parts[0]):
        raise ValidationError(f"Invalid email")
    if domain != allowed_domain:
        raise ValidationError(f"Email must be from the {allowed_domain} domain.")
    
def validate_unique_unity_id(value):
    """
    Ensures the provided Unity ID is unique within the `userDB` collection.

    This function initializes the database connection, if not already initialized, 
    and checks the `userDB` collection to determine if a record with the same 
    Unity ID already exists.

    Args:
        value (str): The Unity ID to validate.

    Raises:
        ValidationError: If a user with the same Unity ID already exists in the database.
    """
    intializeDB()
    unity_user = userDB.find_one({"unityid": value})
    if(unity_user):
        raise ValidationError("Unity ID must be unique")