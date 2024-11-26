from datetime import datetime


class DateUtils:
    @classmethod
    def has_date_passed(cls, date: str) -> bool:
        given_date = datetime.strptime(date, "%Y-%m-%d").date()

        today = datetime.today().date()

        return given_date < today
