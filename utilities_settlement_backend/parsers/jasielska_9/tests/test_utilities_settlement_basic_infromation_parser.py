from datetime import date
from os import path

import pandas as pd
import pytest

from csv_reader import read_csv_file
from datatypes import UtilitiesSettlementBasicInformation
from parsers.jasielska_9.utilities_settlement_basic_information_parser import (
    parse_utilities_settlement_basic_information,
)

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
            "utilities_settlement_basic_information.csv",
            UtilitiesSettlementBasicInformation(
                settlement_period_start_date=date(2025, 1, 1),
                settlement_period_end_date=date(2025, 6, 30),
                settlement_date=date(2025, 9, 1),
                housing_community_name="Jasielska 9, 9B-F",
                street_name="Jasielska",
            ),
        )
    ],
    indirect=["data"],
)
def test_utilities_settlement_basic_information_parser(
    data: pd.DataFrame, expected_parser_output: UtilitiesSettlementBasicInformation
):
    assert parse_utilities_settlement_basic_information(data) == expected_parser_output
