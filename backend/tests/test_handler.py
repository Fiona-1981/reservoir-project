from datetime import date
from handler import merge_week
from models import Reservoir, ReservoirLevels, Week


def make_week(day, carlisle_stock):
    return Week(date=day, reservoirs=[Reservoir(name="Carlisle", actual_stock=carlisle_stock)])

def make_history(*weeks):
    return ReservoirLevels(water_company="United Utilities", weeks=list(weeks))


def test_merge_week_adds_new_week():
    history = make_history(make_week(date(2026, 9, 27), 90.0))
    merged = merge_week(history, make_week(date(2026, 10, 4), 92.3))
    assert [w.date for w in merged.weeks] == [date(2026, 9, 27), date(2026, 10, 4)]


def test_merge_week_same_date_twice_keeps_one_copy_with_newer_values():
    history = make_history()
    merged = merge_week(history, make_week(date(2026, 10, 4), 92.3))
    merged = merge_week(merged, make_week(date(2026, 10, 4), 93.0))
    assert len(merged.weeks) == 1
    assert merged.weeks[0].reservoirs[0].actual_stock == 93.0


def test_merge_week_into_empty_history():
    merged = merge_week(make_history(), make_week(date(2026, 10, 11), 98.7))
    assert merged.water_company == "United Utilities"
    assert [w.date for w in merged.weeks] == [date(2026, 10, 11)]


def test_merge_week_keeps_weeks_sorted_by_date():
    history = make_history(make_week(date(2026, 9, 27), 90.0), make_week(date(2026, 10, 11), 98.7))
    merged = merge_week(history, make_week(date(2026, 10, 4), 92.3))
    assert [w.date for w in merged.weeks] == [date(2026, 9, 27), date(2026, 10, 4), date(2026, 10, 11)]


def test_merge_week_does_not_change_original_history():
    history = make_history(make_week(date(2026, 9, 27), 90.0))
    merge_week(history, make_week(date(2026, 10, 4), 92.3))
    assert [w.date for w in history.weeks] == [date(2026, 9, 27)]
