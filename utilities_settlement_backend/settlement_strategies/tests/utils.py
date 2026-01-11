from datetime import date
from typing import Any

from datatypes import (
    UtilityType,
    UtilitySettlementInputWithMeters,
    MeterReadingInterval,
    UtilitySettlementInputWithoutMeters,
    FlatInformation,
    FlatSettlementInput,
    UtilitiesSettlementForFlat,
    UtilitySettlementOutputWithoutMeters,
    UtilitySettlementOutputWithMeters,
    UtilitySettlementOutputWithoutAdvancePayment,
    UtilitiesSettlementBasicInformation,
)


def generate_flat_settlement_input(
    input_data: dict[str, dict[str, Any]],
) -> list[FlatSettlementInput]:
    settlement_input = []
    for key, input_dict in input_data.items():
        settlement_input.append(
            FlatSettlementInput(
                flat_information=FlatInformation(
                    building_number=input_dict["building_number"],
                    flat_number=input_dict["flat_number"],
                    flat_size=input_dict["flat_size"],
                    laf_factor=input_dict["laf_factor"],
                ),
                utilities_settlement_input_without_meters={
                    UtilityType.CO_FIXED_FEE: UtilitySettlementInputWithoutMeters(
                        utility_type=UtilityType.CO_FIXED_FEE,
                        advance_payment=input_dict["co_fixed_fee_advance_payment"],
                    ),
                },
                utilities_settlement_input_with_meters={
                    UtilityType.ZW: UtilitySettlementInputWithMeters(
                        utility_type=UtilityType.ZW,
                        advance_payment=input_dict["zw_advance_payment"],
                        meters_readings=[
                            MeterReadingInterval(
                                meter_number=f"zw_{input_dict["building_number"]}_{input_dict["flat_number"]}",
                                current_date=date(2025, 6, 15),
                                current_value=input_dict["zw_usage"],
                                previous_date=date(2024, 12, 15),
                                previous_value=0,
                            )
                        ],
                    ),
                    UtilityType.CW: UtilitySettlementInputWithMeters(
                        utility_type=UtilityType.CW,
                        advance_payment=input_dict["cw_advance_payment"],
                        meters_readings=[
                            MeterReadingInterval(
                                meter_number=f"cw_{input_dict["building_number"]}_{input_dict["flat_number"]}",
                                current_date=date(2025, 6, 15),
                                current_value=input_dict["cw_usage"],
                                previous_date=date(2024, 12, 15),
                                previous_value=0,
                            )
                        ],
                    ),
                    UtilityType.CO: UtilitySettlementInputWithMeters(
                        utility_type=UtilityType.CO,
                        advance_payment=input_dict["co_advance_payment"],
                        meters_readings=[
                            MeterReadingInterval(
                                meter_number=f"co_{input_dict["building_number"]}_{input_dict["flat_number"]}",
                                current_date=date(2025, 6, 15),
                                current_value=input_dict["co_usage"],
                                previous_date=date(2024, 12, 15),
                                previous_value=0,
                            )
                        ],
                    ),
                },
            )
        )
    return settlement_input


def generate_flat_settlement_output(
    output_data: dict[str, dict[str, Any]],
) -> list[UtilitiesSettlementForFlat]:
    settlement_output = []

    for key, output_dict in output_data.items():
        settlement_output.append(
            UtilitiesSettlementForFlat(
                flat_information=FlatInformation(
                    building_number=output_dict["building_number"],
                    flat_number=output_dict["flat_number"],
                    flat_size=output_dict["flat_size"],
                    laf_factor=output_dict["laf_factor"],
                ),
                settlement_basic_information=UtilitiesSettlementBasicInformation(
                    settlement_period_start_date=date(2025, 1, 1),
                    settlement_period_end_date=date(2025, 6, 30),
                    settlement_date=date(2025, 9, 15),
                    housing_community_name="Jasielska 9, 9B-F",
                    street_name="Jasielska",
                ),
                utilities_settlement_without_advance_payment={
                    UtilityType.COMMON_AREAS_FEE: UtilitySettlementOutputWithoutAdvancePayment(
                        utility_type=UtilityType.COMMON_AREAS_FEE,
                        actual_cost=output_dict["common_areas_fee_actual_cost"],
                    ),
                },
                utilities_settlement_without_meters={
                    UtilityType.CO_FIXED_FEE: UtilitySettlementOutputWithoutMeters(
                        utility_type=UtilityType.CO_FIXED_FEE,
                        actual_cost=output_dict["co_fixed_fee_actual_cost"],
                        advance_payment=output_dict["co_fixed_fee_advance_payment"],
                        advance_payment_per_unit=output_dict[
                            "co_fixed_fee_advance_payment_per_unit"
                        ],
                        actual_cost_per_unit=output_dict[
                            "co_fixed_fee_actual_cost_per_unit"
                        ],
                        unit="m^2",
                    ),
                },
                utilities_settlement_with_meters={
                    UtilityType.ZW: UtilitySettlementOutputWithMeters(
                        utility_type=UtilityType.ZW,
                        actual_cost=output_dict["zw_actual_cost"],
                        advance_payment=output_dict["zw_advance_payment"],
                        advance_payment_per_unit=output_dict[
                            "zw_advance_payment_per_unit"
                        ],
                        meters_readings=[
                            MeterReadingInterval(
                                meter_number=f"zw_{output_dict["building_number"]}_{output_dict["flat_number"]}",
                                current_date=date(2025, 6, 15),
                                current_value=output_dict["zw_usage"],
                                previous_date=date(2024, 12, 15),
                                previous_value=0,
                            )
                        ],
                        actual_cost_per_unit=output_dict["zw_actual_cost_per_unit"],
                        unit="m^3",
                    ),
                    UtilityType.CW: UtilitySettlementOutputWithMeters(
                        utility_type=UtilityType.CW,
                        actual_cost=output_dict["cw_actual_cost"],
                        advance_payment=output_dict["cw_advance_payment"],
                        advance_payment_per_unit=output_dict[
                            "cw_advance_payment_per_unit"
                        ],
                        meters_readings=[
                            MeterReadingInterval(
                                meter_number=f"cw_{output_dict["building_number"]}_{output_dict["flat_number"]}",
                                current_date=date(2025, 6, 15),
                                current_value=output_dict["cw_usage"],
                                previous_date=date(2024, 12, 15),
                                previous_value=0,
                            )
                        ],
                        actual_cost_per_unit=output_dict["cw_actual_cost_per_unit"],
                        unit="m^3",
                    ),
                    UtilityType.CO: UtilitySettlementOutputWithMeters(
                        utility_type=UtilityType.CO,
                        actual_cost=output_dict["co_actual_cost"],
                        advance_payment=output_dict["co_advance_payment"],
                        advance_payment_per_unit=output_dict[
                            "co_advance_payment_per_unit"
                        ],
                        meters_readings=[
                            MeterReadingInterval(
                                meter_number=f"co_{output_dict["building_number"]}_{output_dict["flat_number"]}",
                                current_date=date(2025, 6, 15),
                                current_value=output_dict["co_usage"],
                                previous_date=date(2024, 12, 15),
                                previous_value=0,
                            )
                        ],
                        actual_cost_per_unit=output_dict["co_actual_cost_per_unit"],
                        unit="GJ",
                    ),
                },
            )
        )

    return settlement_output
