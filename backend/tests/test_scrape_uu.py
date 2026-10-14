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

@pytest.fixture
def week(uu_html):
    return parse_table(uu_html)

def find_reservoir(week, name):
    return next(r for r in week.reservoirs if r.name == name)

def test_parse_table_date(week):
    assert week.date == date(2026, 9, 27)

def test_parse_table_includes_every_row(week):
    assert len(week.reservoirs) == 5
    assert find_reservoir(week, "Regional Total").actual_stock == 52.9

def test_parse_table_actual_stock(week):
    assert find_reservoir(week, "Carlisle").actual_stock == 90.0

def test_parse_table_maps_all_value_columns(week):
    carlisle = find_reservoir(week, "Carlisle")
    assert carlisle.change_since_last_week == -10.0
    assert carlisle.average_year == 86.3
    assert carlisle.last_year == 98.7

def test_parse_table_cell_with_stray_p_tag(week):
    assert find_reservoir(week, "Haweswater & Thirlmere").average_year == 62.3


def test_parse_table_rejects_page_without_table():
    with pytest.raises(ValueError, match="No table"):
        parse_table("<p>No table here</p>")

def test_parse_table_rejects_unexpected_header(uu_html):
    html = uu_html.replace("Last year", "Last month")
    with pytest.raises(ValueError, match="header"):
        parse_table(html)

def test_parse_table_rejects_row_with_missing_value(uu_html):
    html = uu_html.replace("<td>98.7%</td>", "", 1)
    with pytest.raises(ValueError, match="Carlisle"):
        parse_table(html)

