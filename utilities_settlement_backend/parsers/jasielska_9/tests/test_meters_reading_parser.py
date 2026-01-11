from datetime import date
from os import path

import pandas as pd
import pytest

from csv_reader import read_csv_file
from datatypes import FlatId, MeterReading, UtilityType
from parsers.jasielska_9.meters_reading_parser import parse_meter_readings

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
            "meters_reading_2025_06_15.csv",
            {
                "9_1": [
                    MeterReading(
                        building_number="9",
                        flat_number="1",
                        utility_type=UtilityType.ZW,
                        meter_number="1",
                        date=date(2025, 6, 15),
                        value=20,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="1",
                        utility_type=UtilityType.CW,
                        meter_number="2",
                        date=date(2025, 6, 15),
                        value=5,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="1",
                        utility_type=UtilityType.CO,
                        meter_number="3",
                        date=date(2025, 6, 15),
                        value=6,
                    ),
                ],
                "9_2": [
                    MeterReading(
                        building_number="9",
                        flat_number="2",
                        utility_type=UtilityType.ZW,
                        meter_number="4",
                        date=date(2025, 6, 15),
                        value=25,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="2",
                        utility_type=UtilityType.CW,
                        meter_number="5",
                        date=date(2025, 6, 15),
                        value=6,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="2",
                        utility_type=UtilityType.CO,
                        meter_number="6",
                        date=date(2025, 6, 15),
                        value=6,
                    ),
                ],
                "9_3": [
                    MeterReading(
                        building_number="9",
                        flat_number="3",
                        utility_type=UtilityType.ZW,
                        meter_number="7",
                        date=date(2025, 6, 15),
                        value=30,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="3",
                        utility_type=UtilityType.CW,
                        meter_number="8",
                        date=date(2025, 6, 15),
                        value=7,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="3",
                        utility_type=UtilityType.CO,
                        meter_number="9",
                        date=date(2025, 6, 15),
                        value=9,
                    ),
                ],
                "9_4": [
                    MeterReading(
                        building_number="9",
                        flat_number="4",
                        utility_type=UtilityType.ZW,
                        meter_number="10",
                        date=date(2025, 6, 15),
                        value=25,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="4",
                        utility_type=UtilityType.CW,
                        meter_number="11",
                        date=date(2025, 6, 15),
                        value=6,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="4",
                        utility_type=UtilityType.CO,
                        meter_number="12",
                        date=date(2025, 6, 15),
                        value=9,
                    ),
                ],
                "9_5": [
                    MeterReading(
                        building_number="9",
                        flat_number="5",
                        utility_type=UtilityType.ZW,
                        meter_number="13",
                        date=date(2025, 6, 15),
                        value=40,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="5",
                        utility_type=UtilityType.CW,
                        meter_number="14",
                        date=date(2025, 6, 15),
                        value=14,
                    ),
                    MeterReading(
                        building_number="9",
                        flat_number="5",
                        utility_type=UtilityType.CO,
                        meter_number="15",
                        date=date(2025, 6, 15),
                        value=12,
                    ),
                ],
            },
        )
    ],
    indirect=["data"],
)
def test_meter_reading_parser(
    data: pd.DataFrame, expected_parser_output: dict[FlatId, list[MeterReading]]
):
    assert (
        parse_meter_readings(data, meter_reading_date_str="2025-06-15")
        == expected_parser_output
    )
