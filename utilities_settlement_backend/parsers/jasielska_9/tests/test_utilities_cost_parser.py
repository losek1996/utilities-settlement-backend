from os import path

import pandas as pd
import pytest

from csv_reader import read_csv_file
from datatypes import (
    UtilitiesCost,
    UtilityType,
    UtilityWithoutMetersCost,
    UtilityWithMetersCost,
)
from parsers.jasielska_9.utilities_cost_parser import parse_utilities_cost

DATA_DIR = path.join(
    path.dirname(path.realpath(__file__)),
    "data",
)


@pytest.fixture
def data(request) -> pd.DataFrame:
    return read_csv_file(path.join(DATA_DIR, request.param))


@pytest.mark.parametrize(
    "data, expected_parser_output",
    [
        pytest.param(
            "utilities_cost_2025_06_15.csv",
            UtilitiesCost(
                utilities_without_meters_cost={
                    UtilityType.HEAT_ENERGY_FIXED_FEE: UtilityWithoutMetersCost(
                        utility_type=UtilityType.HEAT_ENERGY_FIXED_FEE,
                        total_cost=2500,
                    ),
                },
                utilities_with_meters_cost={
                    UtilityType.ZW: UtilityWithMetersCost(
                        utility_type=UtilityType.ZW,
                        unit_type="m3",
                        total_cost=1988,
                        number_of_units=190,
                    ),
                    UtilityType.HEAT_ENERGY: UtilityWithMetersCost(
                        utility_type=UtilityType.HEAT_ENERGY,
                        unit_type="GJ",
                        total_cost=6140,
                        number_of_units=60,
                    ),
                },
            ),
        )
    ],
    indirect=["data"],
)
def test_utilities_cost_parser(
    data: pd.DataFrame, expected_parser_output: UtilitiesCost
):
    assert parse_utilities_cost(data) == expected_parser_output
