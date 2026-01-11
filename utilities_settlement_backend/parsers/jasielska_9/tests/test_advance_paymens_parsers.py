from os import path

import pandas as pd
import pytest

from csv_reader import read_csv_file
from datatypes import AdvancePayment, AdvancePaymentPerUnit, FlatId, UtilityType
from parsers.jasielska_9.advance_payments_parsers import (
    parse_advance_payments,
    parse_advance_payments_per_unit,
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
            "advance_payments.csv",
            {
                "9_1": {
                    UtilityType.ZW: AdvancePayment(
                        building_number="9",
                        flat_number="1",
                        utility_type=UtilityType.ZW,
                        advance_payment=400,
                    ),
                    UtilityType.CW: AdvancePayment(
                        building_number="9",
                        flat_number="1",
                        utility_type=UtilityType.CW,
                        advance_payment=400,
                    ),
                    UtilityType.CO: AdvancePayment(
                        building_number="9",
                        flat_number="1",
                        utility_type=UtilityType.CO,
                        advance_payment=600,
                    ),
                    UtilityType.CO_FIXED_FEE: AdvancePayment(
                        building_number="9",
                        flat_number="1",
                        utility_type=UtilityType.CO_FIXED_FEE,
                        advance_payment=300,
                    ),
                },
                "9_2": {
                    UtilityType.ZW: AdvancePayment(
                        building_number="9",
                        flat_number="2",
                        utility_type=UtilityType.ZW,
                        advance_payment=500,
                    ),
                    UtilityType.CW: AdvancePayment(
                        building_number="9",
                        flat_number="2",
                        utility_type=UtilityType.CW,
                        advance_payment=600,
                    ),
                    UtilityType.CO: AdvancePayment(
                        building_number="9",
                        flat_number="2",
                        utility_type=UtilityType.CO,
                        advance_payment=600,
                    ),
                    UtilityType.CO_FIXED_FEE: AdvancePayment(
                        building_number="9",
                        flat_number="2",
                        utility_type=UtilityType.CO_FIXED_FEE,
                        advance_payment=350,
                    ),
                },
                "9_3": {
                    UtilityType.ZW: AdvancePayment(
                        building_number="9",
                        flat_number="3",
                        utility_type=UtilityType.ZW,
                        advance_payment=500,
                    ),
                    UtilityType.CW: AdvancePayment(
                        building_number="9",
                        flat_number="3",
                        utility_type=UtilityType.CW,
                        advance_payment=700,
                    ),
                    UtilityType.CO: AdvancePayment(
                        building_number="9",
                        flat_number="3",
                        utility_type=UtilityType.CO,
                        advance_payment=600,
                    ),
                    UtilityType.CO_FIXED_FEE: AdvancePayment(
                        building_number="9",
                        flat_number="3",
                        utility_type=UtilityType.CO_FIXED_FEE,
                        advance_payment=400,
                    ),
                },
                "9_4": {
                    UtilityType.ZW: AdvancePayment(
                        building_number="9",
                        flat_number="4",
                        utility_type=UtilityType.ZW,
                        advance_payment=400,
                    ),
                    UtilityType.CW: AdvancePayment(
                        building_number="9",
                        flat_number="4",
                        utility_type=UtilityType.CW,
                        advance_payment=600,
                    ),
                    UtilityType.CO: AdvancePayment(
                        building_number="9",
                        flat_number="4",
                        utility_type=UtilityType.CO,
                        advance_payment=600,
                    ),
                    UtilityType.CO_FIXED_FEE: AdvancePayment(
                        building_number="9",
                        flat_number="4",
                        utility_type=UtilityType.CO_FIXED_FEE,
                        advance_payment=450,
                    ),
                },
                "9_5": {
                    UtilityType.ZW: AdvancePayment(
                        building_number="9",
                        flat_number="5",
                        utility_type=UtilityType.ZW,
                        advance_payment=600,
                    ),
                    UtilityType.CW: AdvancePayment(
                        building_number="9",
                        flat_number="5",
                        utility_type=UtilityType.CW,
                        advance_payment=600,
                    ),
                    UtilityType.CO: AdvancePayment(
                        building_number="9",
                        flat_number="5",
                        utility_type=UtilityType.CO,
                        advance_payment=600,
                    ),
                    UtilityType.CO_FIXED_FEE: AdvancePayment(
                        building_number="9",
                        flat_number="5",
                        utility_type=UtilityType.CO_FIXED_FEE,
                        advance_payment=500,
                    ),
                },
            },
        )
    ],
    indirect=["data"],
)
def test_advance_payments_parser(
    data: pd.DataFrame,
    expected_parser_output: dict[FlatId, dict[UtilityType, AdvancePayment]],
):
    assert parse_advance_payments(data) == expected_parser_output


@pytest.mark.parametrize(
    "data, expected_parser_output",
    [
        pytest.param(
            "advance_payments_per_unit.csv",
            {
                UtilityType.ZW: AdvancePaymentPerUnit(
                    utility_type=UtilityType.ZW,
                    unit="m^3",
                    advance_payment_per_unit=16,
                ),
                UtilityType.CW: AdvancePaymentPerUnit(
                    utility_type=UtilityType.CW,
                    unit="m^3",
                    advance_payment_per_unit=54,
                ),
                UtilityType.CO: AdvancePaymentPerUnit(
                    utility_type=UtilityType.CO,
                    unit="GJ",
                    advance_payment_per_unit=140,
                ),
                UtilityType.CO_FIXED_FEE: AdvancePaymentPerUnit(
                    utility_type=UtilityType.CO_FIXED_FEE,
                    unit="m^2",
                    advance_payment_per_unit=1.5,
                ),
            },
        )
    ],
    indirect=["data"],
)
def test_advance_payments_per_unit_parser(
    data: pd.DataFrame,
    expected_parser_output: dict[UtilityType, AdvancePaymentPerUnit],
):
    assert parse_advance_payments_per_unit(data) == expected_parser_output
