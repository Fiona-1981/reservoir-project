import datetime
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ContractModel(BaseModel):
    # Python uses snake_case (actual_stock), the JSON contract uses camelCase
    # (actualStock). This is the one place that translates between them.
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
        serialize_by_alias=True,
    )


class Reservoir(ContractModel):
    name: str
    actual_stock: float
    # Optional so that JSON written before these fields existed still loads
    change_since_last_week: float | None = None
    average_year: float | None = None
    last_year: float | None = None


class Week(ContractModel):
    date: datetime.date
    reservoirs: list[Reservoir]


class ReservoirLevels(ContractModel):
    water_company: str
    weeks: list[Week]
