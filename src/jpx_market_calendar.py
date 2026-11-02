"""JPX cash-market calendar for paper-only scheduling and stale-data checks.

Covers recurring Japanese national holidays (2026 onward), substitutes,
citizens' holidays, and JPX year-end closures. Exceptional exchange closures
must still be verified against JPX's official calendar by the observer.
"""
from datetime import date, timedelta


def _nth_monday(year: int, month: int, n: int) -> date:
    first = date(year, month, 1)
    return first + timedelta(days=(7 - first.weekday()) % 7 + 7 * (n - 1))


def _national_holidays(year: int) -> set[date]:
    if not 2020 <= year <= 2099:
        raise ValueError("Japanese holiday formulas supported only for 2020-2099")
    vernal = int(20.8431 + 0.242194 * (year - 1980) - (year - 1980) // 4)
    autumnal = int(23.2488 + 0.242194 * (year - 1980) - (year - 1980) // 4)
    holidays = {
        date(year, 1, 1), date(year, 2, 11), date(year, 2, 23),
        date(year, 3, vernal), date(year, 4, 29), date(year, 5, 3),
        date(year, 5, 4), date(year, 5, 5), date(year, 8, 11),
        date(year, 9, autumnal), date(year, 11, 3), date(year, 11, 23),
        _nth_monday(year, 1, 2), _nth_monday(year, 7, 3),
        _nth_monday(year, 9, 3), _nth_monday(year, 10, 2),
    }
    # Substitute holidays for Sundays; the next non-holiday day is closed.
    for holiday in sorted(holidays.copy()):
        if holiday.weekday() == 6:
            substitute = holiday + timedelta(days=1)
            while substitute in holidays:
                substitute += timedelta(days=1)
            holidays.add(substitute)
    # A day between two national holidays is also a public holiday.
    start, end = date(year, 1, 2), date(year, 12, 30)
    day = start
    while day <= end:
        if day not in holidays and day - timedelta(days=1) in holidays and day + timedelta(days=1) in holidays:
            holidays.add(day)
        day += timedelta(days=1)
    return holidays


def is_jpx_session(day: date) -> bool:
    if day.weekday() >= 5:
        return False
    if day.month == 12 and day.day == 31:
        return False
    if day.month == 1 and day.day in (2, 3):
        return False
    return day not in _national_holidays(day.year)
