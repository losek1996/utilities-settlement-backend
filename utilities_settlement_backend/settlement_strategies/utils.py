from datetime import date


AVG_DAYS_IN_MONTH = 30


def get_number_of_months_between_dates(start_date: date, end_date: date) -> int:
    """Rounds to int."""
    return round((end_date - start_date).days / 30)


def round_number(number: float, ndigits: int = 2) -> float:
    return round(number, ndigits=ndigits)
