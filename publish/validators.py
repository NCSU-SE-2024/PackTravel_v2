from datetime import datetime
from django.forms import ValidationError


def validate_date(value):
    given_date = datetime.strptime(value, "%Y-%m-%d").date()

    today = datetime.today().date()

    if given_date < today:
        raise ValidationError(f"Date cannot be of the past")

    if (given_date - today).days > 30:
        raise ValidationError(
            f"Date cannot be more than 30 days in the future")
