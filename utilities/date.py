"""
Module for date utility functions.

This module contains the `DateUtils` class, which provides utility functions
for working with dates. The primary function is to check whether a given date
has passed compared to the current date.

Functions:
    DateUtils:
        - has_date_passed: Checks if a given date has passed compared to today's date.
"""

from datetime import datetime


class DateUtils:
    """
    A utility class for working with dates.

    Provides methods to perform common date-related operations, such as checking
    if a given date has passed compared to the current date.

    Methods:
        has_date_passed(date: str) -> bool:
            Checks if the given date has passed compared to today's date.
    """

    @classmethod
    def has_date_passed(cls, date: str) -> bool:
        """
        Checks if the given date has passed compared to today's date.

        Args:
            date (str): The date to check, formatted as "YYYY-MM-DD".

        Returns:
            bool: True if the given date has passed, False otherwise.
        """
        given_date = datetime.strptime(date, "%Y-%m-%d").date()

        today = datetime.today().date()

        return given_date < today
