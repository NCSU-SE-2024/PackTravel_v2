"""
Validation Module

This module contains various utility functions for validating user input,
specifically for email, Unity ID, username, and password. It also includes
a function for initializing the connection to the MongoDB database, where
user data is stored. The module helps ensure that user-provided data follows
specific rules, such as uniqueness and format, and provides appropriate
error messages when data validation fails.
"""

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
    if userDB is None:
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
    allowed_domain = "ncsu.edu"
    email_parts = value.split("@")
    domain = email_parts[-1]
    if len(email_parts) != 2:
        raise ValidationError(f"Invalid email")
    if not pattern.match(email_parts[0]):
        raise ValidationError(f"Invalid email")
    if domain != allowed_domain:
        raise ValidationError(
            f"Email must be from the {allowed_domain} domain.")


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
    if unity_user:
        raise ValidationError("Unity ID must be unique")


def validate_unique_username(value):
    """
    Ensures the provided username is unique within the `userDB` collection.

    This function initializes the database connection, if not already initialized,
    and checks the `userDB` collection to determine if a record with the same
    username already exists.

    Args:
        value (str): The username to validate.

    Raises:
        ValidationError: If a user with the same username already exists in the database.
    """
    intializeDB()
    unity_user = userDB.find_one({"username": value})
    if unity_user:
        raise ValidationError("Username must be unique")


def validate_password(value):
    """
    Validates the provided password against several security criteria.

    This function checks that the password meets the following criteria:
    - Minimum length of 8 characters and maximum length of 16 characters.
    - At least one lowercase letter.
    - At least one uppercase letter.
    - At least one digit.
    - At least one special character (e.g., `!@#$%^&*()`).
    - It is not a common password.
    - It does not contain repeated characters (e.g., "aaa").

    Args:
        value (str): The password to validate.

    Raises:
        ValidationError: If the password does not meet the required criteria.
    """
    if len(value) < 8:
        raise ValidationError(f"Password is too short")

    elif len(value) > 16:
        raise ValidationError(f"Password is too long")

    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", value):
        raise ValidationError(
            "Password must contain at least one lowercase letter.")

    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", value):
        raise ValidationError(
            "Password must contain at least one uppercase letter.")

    # Check for at least one digit
    if not re.search(r"\d", value):
        raise ValidationError("Password must contain at least one digit.")

    # Check for at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        raise ValidationError(
            "Password must contain at least one special character.")

    # Check for common passwords
    common_passwords = ["password!123456", "12345678", "qwerty", "admin"]
    if value.lower() in common_passwords:
        raise ValidationError(
            "This password is too common. Please choose a more unique password."
        )

    # Check for repeated characters
    if re.search(r"(.)\1{2,}", value):
        raise ValidationError(
            "Password contains repeated characters. Please avoid easily guessable patterns."
        )
