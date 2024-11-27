"""
This module contains test cases for validating the functionality of the RideForm in the publish application.

The test cases verify various scenarios for form validation, including:
- Valid ride data
- Invalid date formats
- Past and future dates
- Invalid destination input

Each test checks the form's behavior and asserts that appropriate validation errors are raised when needed.

Dependencies:
- `django.test.TransactionTestCase`: Provides a test case that allows database transactions to be rolled back after each test.

This module is intended for use with Django's testing framework to ensure that the form behaves as expected under different conditions.
"""

from django.test import TransactionTestCase
from publish.forms import RideForm


class TestForms(TransactionTestCase):
    """
    Test suite for the RideForm form in the publish application.

    This class contains various test cases that check if the RideForm correctly handles valid and invalid input data. Each test method provides different sets of data to the form and asserts whether the form behaves as expected.

    Tests cover scenarios such as:
    - Valid data submission
    - Invalid date formats (including past and future dates)
    - Invalid destination input (source and destination being the same)

    The tests are designed to ensure that the form raises the appropriate validation errors when data does not meet the required criteria.

    This class extends `TransactionTestCase`, which allows tests to interact with the database and ensure data integrity during tests.
    """

    def test_rideform_validData(self):
        """
        Tests the form with valid ride data.

        This test ensures that when a form is submitted with valid data (including source, destination, purpose, rideDate, route, and routeDetails), the form should be valid.

        Asserts:
            - `form.is_valid()` is True, meaning the form passes all validation checks.
        """

        form = RideForm(
            data={
                "source": "1505,Avery Close",
                "destination": "Talley Union",
                "purpose": "Travel",
                "rideDate": "2024-12-15",
                "route": "Bus",
                "routeDetails": "Home to College",
            }
        )
        self.assertTrue(form.is_valid())

    def test_rideform_invalidDate(self):
        """
        Tests the form with an invalid ride date.

        This test provides an invalid date (April 12, 2024) and ensures that the form raises a validation error for the `rideDate` field.

        Asserts:
            - `form.is_valid()` is False, meaning the form fails validation.
            - `rideDate` is included in the form errors.
        """

        form = RideForm(
            data={
                "source": "1505,Avery Close",
                "destination": "Talley Union",
                "purpose": "Travel",
                "rideDate": "2024-04-12",
                "route": "Bus",
                "routeDetails": "Home to College",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("rideDate", form.errors)

    def test_rideform_pastDate(self):
        """
        Tests the form with a past ride date.

        This test provides a ride date in the past (October 11, 2024) and ensures that the form raises a validation error for the `rideDate` field.

        Asserts:
            - `form.is_valid()` is False, meaning the form fails validation.
            - `rideDate` is included in the form errors.
        """

        form = RideForm(
            data={
                "source": "1505,Avery Close",
                "destination": "Talley Union",
                "purpose": "Travel",
                "rideDate": "2024-10-11",
                "route": "Bus",
                "routeDetails": "Home to College",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("rideDate", form.errors)

    def test_rideform_futureDate(self):
        """
        Tests the form with a future ride date.

        This test provides a ride date in the future (October 11, 2025) and ensures that the form raises a validation error for the `rideDate` field.

        Asserts:
            - `form.is_valid()` is False, meaning the form fails validation.
            - `rideDate` is included in the form errors.
        """
        form = RideForm(
            data={
                "source": "1505,Avery Close",
                "destination": "Talley Union",
                "purpose": "Travel",
                "rideDate": "2025-10-11",
                "route": "Bus",
                "routeDetails": "Home to College",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("rideDate", form.errors)

    def test_rideform_invalidDestination(self):
        """
        Tests the form with invalid source and destination values.

        This test checks that when the source and destination are the same (e.g., '1505, Avery Close'), the form raises a validation error for the `destination` field. The test verifies that the custom validation logic prevents users from entering identical source and destination locations.

        Asserts:
            - `form.is_valid()` is False, meaning the form fails validation.
            - The error message `'Source and destination must be different.'` is included in the form's `__all__` errors.
        """

        form = RideForm(
            data={
                "source": "1505,Avery Close",
                "destination": "1505,Avery Close",
                "purpose": "Travel",
                "rideDate": "2024-11-15",
                "route": "Bike",
                "routeDetails": "Home to College",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Source and destination must be different.", form.errors["__all__"]
        )
