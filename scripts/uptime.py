"""
Recalculates the 'uptime' line in README.md as the calendar-accurate time
elapsed since START_DATE, then rewrites that one line in place.

No third-party dependencies — uses only stdlib (datetime + calendar) so the
GitHub Actions workflow doesn't need a pip install step.
"""

import calendar
import re
from datetime import date
from pathlib import Path

START_DATE = date(2022, 3, 26)
README_PATH = Path(__file__).resolve().parent.parent / "README.md"


def diff_ymd(start: date, end: date) -> tuple[int, int, int]:
    """Calendar-accurate (years, months, days) between two dates."""
    years = end.year - start.year
    months = end.month - start.month
    days = end.day - start.day

    if days < 0:
        months -= 1
        prev_month = end.month - 1 or 12
        prev_year = end.year if end.month > 1 else end.year - 1
        days += calendar.monthrange(prev_year, prev_month)[1]

    if months < 0:
        years -= 1
        months += 12

    return years, months, days


def format_uptime(years: int, months: int, days: int) -> str:
    parts = []
    if years:
        parts.append(f"{years}y")
    if months:
        parts.append(f"{months}m")
    parts.append(f"{days}d")
    return " ".join(parts)


def main() -> None:
    today = date.today()
    years, months, days = diff_ymd(START_DATE, today)
    uptime_str = format_uptime(years, months, days)
    new_line = f"uptime: {uptime_str} (since {START_DATE.strftime('%d %b %Y').lower()})"

    content = README_PATH.read_text(encoding="utf-8")
    new_content, count = re.subn(
        r"^uptime:.*$", new_line, content, count=1, flags=re.MULTILINE
    )

    if count == 0:
        raise SystemExit("No 'uptime:' line found in README.md — check the yaml block.")

    if new_content != content:
        README_PATH.write_text(new_content, encoding="utf-8")
        print(f"Updated: {new_line}")
    else:
        print("Already up to date.")


if __name__ == "__main__":
    main()
