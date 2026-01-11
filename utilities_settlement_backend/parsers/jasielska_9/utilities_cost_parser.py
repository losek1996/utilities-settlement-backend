import pandas as pd

from datatypes import (
    UtilitiesCost,
    UtilityWithoutMetersCost,
    UtilityType,
    UtilityWithMetersCost,
)
from parsers.utils import replace_nan_with_none


def parse_utilities_cost(data: pd.DataFrame) -> UtilitiesCost:
    # Replace NaN values with None for proper Pydantic validation
    data = data.where(pd.notna(data), None)
    utilities_cost_rows = data.to_dict(orient="records")

    utilities_without_meters_cost: dict[UtilityType, UtilityWithoutMetersCost] = {}
    utilities_with_meters_cost: dict[UtilityType, UtilityWithMetersCost] = {}
    for row in utilities_cost_rows:
        cleaned_row = replace_nan_with_none(row)
        if cleaned_row["unit_type"] is None:
            utility_with_cost = UtilityWithoutMetersCost.model_validate(cleaned_row)
            utilities_without_meters_cost[utility_with_cost.utility_type] = (
                utility_with_cost
            )
        else:
            utility_with_cost = UtilityWithMetersCost.model_validate(cleaned_row)
            utilities_with_meters_cost[utility_with_cost.utility_type] = (
                utility_with_cost
            )

    return UtilitiesCost(
        utilities_without_meters_cost=utilities_without_meters_cost,
        utilities_with_meters_cost=utilities_with_meters_cost,
    )
