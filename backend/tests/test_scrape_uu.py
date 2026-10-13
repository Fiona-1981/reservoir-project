from datetime import date
from pathlib import Path
import pytest
from scrape_uu import parse_percent, parse_date, parse_table

FIXTURES = Path(__file__).parent / "fixtures"

@pytest.mark.parametrize("text, expected", [
    ("27th September 2026", date(2026, 9, 27)),
    ("1st October 2026", date(2026, 10, 1)),
    ("2nd October 2026", date(2026, 10, 2)),
    ("3rd October 2026", date(2026, 10, 3)),
    ("9th September 2026", date(2026, 9, 9)),
    ("22nd February 2026", date(2026, 2, 22)),
])
def test_parse_date(text, expected):
    assert parse_date(text) == expected


def test_parse_date_rejects_bad_date():
    with pytest.raises(ValueError):
        parse_date("31st September 2026")


@pytest.mark.parametrize("text, expected", [
    ("60.2%", 60.2),
    ("-5.7%", -5.7),
    pytest.param("6.2%", 1.0, marks=pytest.mark.xfail(reason="deliberate failure")),
    ("8.93 %", 8.93),
    ("4.895%", 4.895),
])
def test_parse_percent(text, expected):
    assert parse_percent(text) == expected


@pytest.fixture
def uu_html():
    return (FIXTURES / "uu_reservoir_levels.html").read_text(encoding="utf-8")

def test_parse_table(uu_html):
    assert parse_table(uu_html) == date(2026, 9, 27)

