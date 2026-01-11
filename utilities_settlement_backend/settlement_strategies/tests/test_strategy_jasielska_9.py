from datetime import date

import pytest

from datatypes import (
    UtilitiesSettlementBasicInformation,
    AdvancePaymentPerUnit,
    UtilityType,
    UtilitiesCost,
    UtilityWithMetersCost,
    UtilityWithoutMetersCost,
    FlatSettlementInput,
    UtilitiesSettlementForFlat,
)
from settlement_strategies.strategy_jasielska_9 import Jasielska9SettlementStrategy
from settlement_strategies.tests.utils import (
    generate_flat_settlement_input,
    generate_flat_settlement_output,
)


@pytest.fixture
def settlement_basic_information() -> UtilitiesSettlementBasicInformation:
    return UtilitiesSettlementBasicInformation(
        settlement_period_start_date=date(2025, 1, 1),
        settlement_period_end_date=date(2025, 6, 30),
        settlement_date=date(2025, 9, 15),
        housing_community_name="Jasielska 9, 9B-F",
        street_name="Jasielska",
    )


@pytest.fixture
def advance_payments_per_unit() -> dict[UtilityType, AdvancePaymentPerUnit]:
    return {
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
    }


@pytest.fixture
def utilities_cost() -> UtilitiesCost:
    return UtilitiesCost(
        utilities_without_meters_cost={
            UtilityType.HEAT_ENERGY_FIXED_FEE: UtilityWithoutMetersCost(
                utility_type=UtilityType.HEAT_ENERGY_FIXED_FEE,
                total_cost=1536,
            )
        },
        utilities_with_meters_cost={
            UtilityType.ZW: UtilityWithMetersCost(
                utility_type=UtilityType.ZW,
                total_cost=1020,
                unit_type="m^3",
                number_of_units=60,
            ),
            UtilityType.HEAT_ENERGY: UtilityWithMetersCost(
                utility_type=UtilityType.HEAT_ENERGY,
                total_cost=3400,
                unit_type="m^3",
                number_of_units=25,
            ),
        },
    )


@pytest.mark.parametrize(
    "flats_settlement_input, expected_settlement_per_flat",
    [
        pytest.param(
            generate_flat_settlement_input(
                {
                    "9_1": {
                        "building_number": "9",
                        "flat_number": "1",
                        "flat_size": 50,
                        "laf_factor": 0.8,
                        "co_fixed_fee_advance_payment": 450,
                        "zw_advance_payment": 160,
                        "zw_usage": 11,
                        "cw_advance_payment": 270,
                        "cw_usage": 5,
                        "co_advance_payment": 700,
                        "co_usage": 6,
                    },
                    "9_2": {
                        "building_number": "9",
                        "flat_number": "2",
                        "flat_size": 60,
                        "laf_factor": 0.7,
                        "co_fixed_fee_advance_payment": 540,
                        "zw_advance_payment": 192,
                        "zw_usage": 8,
                        "cw_advance_payment": 324,
                        "cw_usage": 4,
                        "co_advance_payment": 840,
                        "co_usage": 4,
                    },
                    "9_3": {
                        "building_number": "9",
                        "flat_number": "3",
                        "flat_size": 50,
                        "laf_factor": 0.5,
                        "co_fixed_fee_advance_payment": 450,
                        "zw_advance_payment": 160,
                        "zw_usage": 12,
                        "cw_advance_payment": 270,
                        "cw_usage": 8,
                        "co_advance_payment": 700,
                        "co_usage": 8,
                    },
                },
            ),
            generate_flat_settlement_output(
                {
                    "9_1": {
                        "building_number": "9",
                        "flat_number": "1",
                        "flat_size": 50,
                        "laf_factor": 0.8,
                        "common_areas_fee_actual_cost": 68,
                        "co_fixed_fee_actual_cost": 480,
                        "co_fixed_fee_advance_payment": 450,
                        "co_fixed_fee_advance_payment_per_unit": 1.5,
                        "co_fixed_fee_actual_cost_per_unit": 1.6,
                        "zw_actual_cost": 187,
                        "zw_advance_payment": 160,
                        "zw_advance_payment_per_unit": 16,
                        "zw_usage": 11,
                        "zw_actual_cost_per_unit": 17,
                        "cw_actual_cost": 365,
                        "cw_advance_payment": 270,
                        "cw_advance_payment_per_unit": 54,
                        "cw_usage": 5,
                        "cw_actual_cost_per_unit": 73,
                        "co_actual_cost": 816,
                        "co_advance_payment": 700,
                        "co_advance_payment_per_unit": 140,
                        "co_usage": 6,
                        "co_actual_cost_per_unit": 136,
                    },
                    "9_2": {
                        "building_number": "9",
                        "flat_number": "2",
                        "flat_size": 60,
                        "laf_factor": 0.7,
                        "common_areas_fee_actual_cost": 68,
                        "co_fixed_fee_actual_cost": 576,
                        "co_fixed_fee_advance_payment": 540,
                        "co_fixed_fee_advance_payment_per_unit": 1.5,
                        "co_fixed_fee_actual_cost_per_unit": 1.6,
                        "zw_actual_cost": 136,
                        "zw_advance_payment": 192,
                        "zw_advance_payment_per_unit": 16,
                        "zw_usage": 8,
                        "zw_actual_cost_per_unit": 17,
                        "cw_actual_cost": 292,
                        "cw_advance_payment": 324,
                        "cw_advance_payment_per_unit": 54,
                        "cw_usage": 4,
                        "cw_actual_cost_per_unit": 73,
                        "co_actual_cost": 544,
                        "co_advance_payment": 840,
                        "co_advance_payment_per_unit": 140,
                        "co_usage": 4,
                        "co_actual_cost_per_unit": 136,
                    },
                    "9_3": {
                        "building_number": "9",
                        "flat_number": "3",
                        "flat_size": 50,
                        "laf_factor": 0.5,
                        "common_areas_fee_actual_cost": 68,
                        "co_fixed_fee_actual_cost": 480,
                        "co_fixed_fee_advance_payment": 450,
                        "co_fixed_fee_advance_payment_per_unit": 1.5,
                        "co_fixed_fee_actual_cost_per_unit": 1.6,
                        "zw_actual_cost": 204,
                        "zw_advance_payment": 160,
                        "zw_advance_payment_per_unit": 16,
                        "zw_usage": 12,
                        "zw_actual_cost_per_unit": 17,
                        "cw_actual_cost": 584,
                        "cw_advance_payment": 270,
                        "cw_advance_payment_per_unit": 54,
                        "cw_usage": 8,
                        "cw_actual_cost_per_unit": 73,
                        "co_actual_cost": 1088,
                        "co_advance_payment": 700,
                        "co_advance_payment_per_unit": 140,
                        "co_usage": 8,
                        "co_actual_cost_per_unit": 136,
                    },
                }
            ),
        )
    ],
)
def test_generate_settlement(
    settlement_basic_information: UtilitiesSettlementBasicInformation,
    advance_payments_per_unit: dict[UtilityType, AdvancePaymentPerUnit],
    utilities_cost: UtilitiesCost,
    flats_settlement_input: list[FlatSettlementInput],
    expected_settlement_per_flat: list[UtilitiesSettlementForFlat],
) -> None:
    assert (
        Jasielska9SettlementStrategy().generate_settlement(
            settlement_basic_information=settlement_basic_information,
            advance_payments_per_unit=advance_payments_per_unit,
            utilities_cost=utilities_cost,
            flats_settlement_input=flats_settlement_input,
            include_laf_factor=False,
        )
        == expected_settlement_per_flat
    )
