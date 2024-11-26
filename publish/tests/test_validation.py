from datetime import datetime
from django.test import SimpleTestCase
from utilities import DateUtils


class DateValidationTests(SimpleTestCase):
    def test_past_date(self):
        self.assertTrue(DateUtils.has_date_passed(
            "2020-01-01"), "Should be False for past date")

    def test_current_date(self):
        current_date = datetime.today().date().strftime("%Y-%m-%d")
        self.assertFalse(DateUtils.has_date_passed(
            current_date), "Should be True for current date")

    def test_future_date(self):
        self.assertFalse(DateUtils.has_date_passed(
            "2025-01-01"), "Should be True for future date")
