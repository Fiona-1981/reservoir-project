import pytest

from scrape_uu import parse_percent
from scrape_uu import parse_date

# def test_parse_date():
#     assert parse_date("9th September 2026") ==

@pytest.mark.parametrize("text, expected", [
    ("60.2%", 60.2),
    ("-5.7%", -5.7),
    pytest.param("6.2%", 1.0, marks=pytest.mark.xfail(reason="deliberate failure")),
    ("8.93 %", 8.93),
    ("4.895%", 4.895),
])
def test_parse_percent(text, expected):
    assert parse_percent(text) == expected
