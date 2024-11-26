"""
This module contains test cases for validating the behavior of date-related utility functions in the 'utilities' package.

Test cases include:
- Verifying whether a given date has passed compared to the current date.

Dependencies:
- `django.test.SimpleTestCase`: For testing without database interaction.
- `datetime`: For working with date and time objects.
- `utilities.DateUtils`: A utility class containing the method `has_date_passed` for date comparison.
"""

from datetime import datetime
from django.test import SimpleTestCase
from utilities import DateUtils


class DateValidationTests(SimpleTestCase):
    """
    Test suite for validating the functionality of the `has_date_passed` method in the `DateUtils` class.

    This class tests various scenarios for the `has_date_passed` method, which checks whether a given date has passed in comparison to the current date.

    Test cases include:
    - Checking if the method correctly identifies a past date.
    - Checking if the method correctly identifies the current date.
    - Checking if the method correctly identifies a future date.

    This class extends `SimpleTestCase` as it does not require database interaction.
    """

    def test_past_date(self):
        """
        Tests the `has_date_passed` method with a past date.

        This test checks if the `has_date_passed` method correctly identifies that the date "2020-01-01" has passed.

        Asserts:
            - The result should be `True` for a past date.
        """

        self.assertTrue(DateUtils.has_date_passed(
            "2020-01-01"), "Should be False for past date")

    def test_current_date(self):
        """
        Tests the `has_date_passed` method with the current date.

        This test checks if the `has_date_passed` method correctly identifies that today's date has not yet passed.

        Asserts:
            - The result should be `False` for the current date.
        """

        current_date = datetime.today().date().strftime("%Y-%m-%d")
        self.assertFalse(DateUtils.has_date_passed(
            current_date), "Should be True for current date")

    def test_future_date(self):
        """
        Tests the `has_date_passed` method with a future date.

        This test checks if the `has_date_passed` method correctly identifies that the date "2025-01-01" is in the future and has not passed.

        Asserts:
            - The result should be `False` for a future date.
        """

        self.assertFalse(DateUtils.has_date_passed(
            "2025-01-01"), "Should be True for future date")
