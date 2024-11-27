"""
Module for custom date validation in forms.

This module defines a custom validator function for date fields. The `validate_date` function ensures that the provided date is neither in the past nor more than 30 days in the future. It raises a `ValidationError` if the date does not meet these criteria.

The `validate_date` function is typically used as a validator in Django form fields.
"""

from datetime import datetime
from django.forms import ValidationError


def validate_date(value):
    """
    Validates the provided date value to ensure it is not in the past or more than 30 days in the future.

    This function checks if the given date is:
    1. Not in the past, i.e., earlier than today's date.
    2. Not more than 30 days into the future from the current date.

    If the date is invalid, a `ValidationError` is raised with an appropriate message.

    Args:
        value (str): The date string to be validated, expected in the format "%Y-%m-%d".

    Raises:
        ValidationError: If the provided date is in the past or more than 30 days in the future.
    """
    given_date = datetime.strptime(value, "%Y-%m-%d").date()

    today = datetime.today().date()

    if given_date < today:
        raise ValidationError(f"Date cannot be of the past")

    if (given_date - today).days > 30:
        raise ValidationError(
            f"Date cannot be more than 30 days in the future")
