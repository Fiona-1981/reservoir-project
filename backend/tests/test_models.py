import json
from datetime import date
from pathlib import Path
import pytest
from models import ReservoirLevels, Reservoir

SAMPLE = Path(__file__).parents[2] / "contract" / "sample.json"


@pytest.fixture
def sample_json():
    return SAMPLE.read_text(encoding="utf-8")


def test_sample_contract_loads_into_snake_case(sample_json):
    levels = ReservoirLevels.model_validate_json(sample_json)
    assert levels.water_company == "United Utilities"
    assert levels.weeks[0].date == date(2026, 9, 26)
    assert levels.weeks[0].reservoirs[0].actual_stock == 91.1


def test_sample_contract_round_trips(sample_json):
    levels = ReservoirLevels.model_validate_json(sample_json)
    assert json.loads(levels.model_dump_json()) == json.loads(sample_json)


def test_serialises_to_camel_case():
    reservoir = Reservoir(
        name="Carlisle",
        actual_stock=90.0,
        change_since_last_week=-10.0,
        average_year=86.3,
        last_year=98.7,
    )
    assert reservoir.model_dump() == {
        "name": "Carlisle",
        "actualStock": 90.0,
        "changeSinceLastWeek": -10.0,
        "averageYear": 86.3,
        "lastYear": 98.7,
    }


def test_loads_json_without_newer_fields():
    reservoir = Reservoir.model_validate_json('{"name": "Carlisle", "actualStock": 90.0}')
    assert reservoir.average_year is None
