from datatypes import (
    FlatSettlementInput,
    UtilitiesCost,
    UtilitiesSettlementForFlat,
    UtilitySettlementOutputWithMeters,
    UtilitySettlementInputWithMeters,
    UtilityType,
    UtilitiesSettlementBasicInformation,
    AdvancePaymentPerUnit,
    UtilitySettlementOutputWithoutMeters,
    UtilityWithMetersCost,
    UtilityWithoutMetersCost,
    FlatInformation,
    UtilitySettlementOutputWithoutAdvancePayment,
    FlatId,
    DEFAULT_LAF_FACTOR,
)
from settlement_strategies.strategy import ISettlementStrategy
from settlement_strategies.utils import get_number_of_months_between_dates, round_number


class Jasielska9SettlementStrategy(ISettlementStrategy):
    def generate_settlement(
        self,
        settlement_basic_information: UtilitiesSettlementBasicInformation,
        advance_payments_per_unit: dict[UtilityType, AdvancePaymentPerUnit],
        utilities_cost: UtilitiesCost,
        flats_settlement_input: list[FlatSettlementInput],
        include_laf_factor: bool,
    ) -> list[UtilitiesSettlementForFlat]:
        utilities_settlement: list[UtilitiesSettlementForFlat] = []

        common_areas_cost_per_flat = self.calculate_common_areas_cost_per_flat(
            utilities_cost, flats_settlement_input
        )
        central_heating_fixed_cost_per_unit = (
            self.get_central_heating_fixed_cost_per_unit(
                settlement_basic_information=settlement_basic_information,
                flats_information=[
                    flat_input.flat_information for flat_input in flats_settlement_input
                ],
                heating_fixed_fee=utilities_cost.utilities_without_meters_cost[
                    UtilityType.HEAT_ENERGY_FIXED_FEE
                ],
            )
        )
        central_heating_cost_per_unit = (
            self.get_central_heating_cost_per_unit_including_laf_factor(
                utilities_cost, flats_settlement_input
            )
            if include_laf_factor
            else utilities_cost.utilities_with_meters_cost[
                UtilityType.HEAT_ENERGY
            ].unit_cost
        )
        water_heating_cost_per_unit = self.get_hot_water_heating_cost_per_unit(
            central_heating_usage_per_flat=[
                flat_input.utilities_settlement_input_with_meters[UtilityType.CO]
                for flat_input in flats_settlement_input
            ],
            hot_water_usage_per_flat=[
                flat_input.utilities_settlement_input_with_meters[UtilityType.CW]
                for flat_input in flats_settlement_input
            ],
            heating_cost=utilities_cost.utilities_with_meters_cost[
                UtilityType.HEAT_ENERGY
            ],
        )
        for flat_settlement_input in flats_settlement_input:
            utilities_settlement.append(
                self.generate_settlement_for_flat(
                    flat_settlement_input=flat_settlement_input,
                    settlement_basic_information=settlement_basic_information,
                    include_laf_factor=include_laf_factor,
                    advance_payments_per_unit=advance_payments_per_unit,
                    utilities_cost=utilities_cost,
                    common_areas_cost_per_flat=common_areas_cost_per_flat,
                    central_heating_cost_per_unit=central_heating_cost_per_unit,
                    central_heating_fixed_cost_per_unit=central_heating_fixed_cost_per_unit,
                    water_heating_cost_per_unit=water_heating_cost_per_unit,
                )
            )

        return utilities_settlement

    @classmethod
    def generate_settlement_for_flat(
        cls,
        flat_settlement_input: FlatSettlementInput,
        settlement_basic_information: UtilitiesSettlementBasicInformation,
        include_laf_factor: bool,
        advance_payments_per_unit: dict[UtilityType, AdvancePaymentPerUnit],
        utilities_cost: UtilitiesCost,
        common_areas_cost_per_flat: float,
        central_heating_cost_per_unit: float,  # unit GJ
        central_heating_fixed_cost_per_unit: float,  # unit m^2
        water_heating_cost_per_unit: float,  # unit m^3
    ) -> UtilitiesSettlementForFlat:
        return UtilitiesSettlementForFlat(
            flat_information=flat_settlement_input.flat_information,
            settlement_basic_information=settlement_basic_information,
            utilities_settlement_without_advance_payment={
                UtilityType.COMMON_AREAS_FEE: UtilitySettlementOutputWithoutAdvancePayment(
                    utility_type=UtilityType.COMMON_AREAS_FEE,
                    actual_cost=common_areas_cost_per_flat,
                ),
            },
            utilities_settlement_without_meters={
                UtilityType.CO_FIXED_FEE: cls.get_central_heating_fixed_fee_settlement_output(
                    settlement_basic_information=settlement_basic_information,
                    advance_payments_per_unit=advance_payments_per_unit,
                    flat_settlement_input=flat_settlement_input,
                    central_heating_fixed_cost_per_unit=central_heating_fixed_cost_per_unit,
                ),
            },
            utilities_settlement_with_meters={
                UtilityType.ZW: cls.get_cold_water_settlement_output(
                    cold_water_usage=flat_settlement_input.utilities_settlement_input_with_meters[
                        UtilityType.ZW
                    ],
                    cold_water_advance_payment_per_unit=advance_payments_per_unit[
                        UtilityType.ZW
                    ],
                    cold_water_cost=utilities_cost.utilities_with_meters_cost[
                        UtilityType.ZW
                    ],
                ),
                UtilityType.CW: cls.get_hot_water_settlement_output(
                    hot_water_usage=flat_settlement_input.utilities_settlement_input_with_meters[
                        UtilityType.CW
                    ],
                    hot_water_advance_payment_per_unit=advance_payments_per_unit[
                        UtilityType.CW
                    ],
                    cold_water_cost=utilities_cost.utilities_with_meters_cost[
                        UtilityType.ZW
                    ],
                    water_heating_cost_per_unit=water_heating_cost_per_unit,
                ),
                UtilityType.CO: cls.get_central_heating_settlement_output(
                    central_heating_usage=flat_settlement_input.utilities_settlement_input_with_meters[
                        UtilityType.CO
                    ],
                    central_heating_advance_payment_per_unit=advance_payments_per_unit[
                        UtilityType.CO
                    ],
                    central_heating_cost_per_unit=central_heating_cost_per_unit,
                    laf_factor=(
                        (
                            flat_settlement_input.flat_information.laf_factor
                            or DEFAULT_LAF_FACTOR
                        )
                        if include_laf_factor
                        else DEFAULT_LAF_FACTOR
                    ),
                ),
            },
        )

    @staticmethod
    def get_hot_water_heating_cost_per_unit(
        central_heating_usage_per_flat: list[UtilitySettlementInputWithMeters],
        hot_water_usage_per_flat: list[UtilitySettlementInputWithMeters],
        heating_cost: UtilityWithMetersCost,
    ) -> float:
        """
        To get cost of heating 1 m^3 of hot water, we have to:
        - calculate energy used to heat water (hot_water_energy = total_energy_from_invoice - energy_used_to_heat_flats)
        - divide energy used to heat water by number of hot water units used and multiply it by heat energy unit cost
        """
        hot_water_total_units = sum(
            [flat.utility_usage_units for flat in hot_water_usage_per_flat]
        )
        central_heating_total_units = sum(
            [flat.utility_usage_units for flat in central_heating_usage_per_flat]
        )

        energy_units_used_to_heat_hot_water = (
            heating_cost.number_of_units - central_heating_total_units
        )

        return round_number(
            heating_cost.unit_cost
            * energy_units_used_to_heat_hot_water
            / hot_water_total_units
        )

    @staticmethod
    def get_central_heating_cost_per_unit_including_laf_factor(
        utilities_cost: UtilitiesCost,
        flats_settlement_input: list[FlatSettlementInput],
    ) -> float:
        """
        LAF factors are not normalized. Normalizing LAF factor could be confusing for residents,
        so we decided to include normalization in price of a central heating single energy unit.
        """

        central_heating_usage_per_flat: dict[FlatId, float] = {
            flat_input.flat_information.flat_id: flat_input.utilities_settlement_input_with_meters[
                UtilityType.CO
            ].utility_usage_units
            for flat_input in flats_settlement_input
        }
        laf_factor_per_flat: dict[FlatId, float] = {
            flat_input.flat_information.flat_id: flat_input.flat_information.laf_factor
            or DEFAULT_LAF_FACTOR
            for flat_input in flats_settlement_input
        }

        cental_heating_total_usage = sum(central_heating_usage_per_flat.values())
        central_heating_total_usage_including_laf_factor = sum(
            flat_usage * laf_factor_per_flat[flat_id]
            for flat_id, flat_usage in central_heating_usage_per_flat.items()
        )

        return (
            utilities_cost.utilities_with_meters_cost[UtilityType.CO].total_cost
            * cental_heating_total_usage
            / central_heating_total_usage_including_laf_factor
        )

    @staticmethod
    def get_central_heating_fixed_cost_per_unit(
        settlement_basic_information: UtilitiesSettlementBasicInformation,
        flats_information: list[FlatInformation],
        heating_fixed_fee: UtilityWithoutMetersCost,
    ) -> float:
        """We need to dived fixed heating fee by sum of all flats sizes."""
        settlement_period_months = get_number_of_months_between_dates(
            settlement_basic_information.settlement_period_start_date,
            settlement_basic_information.settlement_period_end_date,
        )
        return round_number(
            heating_fixed_fee.total_cost
            / sum(flat.flat_size for flat in flats_information)
            / settlement_period_months
        )

    @staticmethod
    def get_central_heating_fixed_fee_per_flat(
        period_months: int,
        central_heating_fixed_cost_per_squared_meter: float,
        flat_size: float,
    ) -> float:
        return round_number(
            central_heating_fixed_cost_per_squared_meter * flat_size * period_months
        )

    @classmethod
    def get_central_heating_fixed_fee_settlement_output(
        cls,
        settlement_basic_information: UtilitiesSettlementBasicInformation,
        advance_payments_per_unit: dict[UtilityType, AdvancePaymentPerUnit],
        flat_settlement_input: FlatSettlementInput,
        central_heating_fixed_cost_per_unit: float,
    ) -> UtilitySettlementOutputWithoutMeters:
        return UtilitySettlementOutputWithoutMeters(
            utility_type=UtilityType.CO_FIXED_FEE,
            actual_cost=cls.get_central_heating_fixed_fee_per_flat(
                period_months=get_number_of_months_between_dates(
                    settlement_basic_information.settlement_period_start_date,
                    settlement_basic_information.settlement_period_end_date,
                ),
                central_heating_fixed_cost_per_squared_meter=central_heating_fixed_cost_per_unit,
                flat_size=flat_settlement_input.flat_information.flat_size,
            ),
            advance_payment=flat_settlement_input.utilities_settlement_input_without_meters[
                UtilityType.CO_FIXED_FEE
            ].advance_payment,
            advance_payment_per_unit=advance_payments_per_unit[
                UtilityType.CO_FIXED_FEE
            ].advance_payment_per_unit,
            actual_cost_per_unit=central_heating_fixed_cost_per_unit,
            unit=advance_payments_per_unit[UtilityType.CO_FIXED_FEE].unit,
        )

    @staticmethod
    def get_cold_water_settlement_output(
        cold_water_usage: UtilitySettlementInputWithMeters,
        cold_water_advance_payment_per_unit: AdvancePaymentPerUnit,
        cold_water_cost: UtilityWithMetersCost,
    ) -> UtilitySettlementOutputWithMeters:
        return UtilitySettlementOutputWithMeters(
            utility_type=UtilityType.ZW,
            actual_cost=round_number(
                cold_water_cost.unit_cost * cold_water_usage.utility_usage_units
            ),
            advance_payment=cold_water_usage.advance_payment,
            advance_payment_per_unit=cold_water_advance_payment_per_unit.advance_payment_per_unit,
            meters_readings=cold_water_usage.meters_readings,
            actual_cost_per_unit=round_number(cold_water_cost.unit_cost),
            unit=cold_water_advance_payment_per_unit.unit,
        )

    @staticmethod
    def get_hot_water_settlement_output(
        hot_water_usage: UtilitySettlementInputWithMeters,
        hot_water_advance_payment_per_unit: AdvancePaymentPerUnit,
        cold_water_cost: UtilityWithMetersCost,
        water_heating_cost_per_unit: float,
    ) -> UtilitySettlementOutputWithMeters:
        hot_water_cost_per_unit = round_number(
            cold_water_cost.unit_cost + water_heating_cost_per_unit
        )
        return UtilitySettlementOutputWithMeters(
            utility_type=UtilityType.CW,
            actual_cost=round_number(
                hot_water_cost_per_unit * hot_water_usage.utility_usage_units
            ),
            advance_payment=hot_water_usage.advance_payment,
            advance_payment_per_unit=hot_water_advance_payment_per_unit.advance_payment_per_unit,
            meters_readings=hot_water_usage.meters_readings,
            actual_cost_per_unit=hot_water_cost_per_unit,
            unit=hot_water_advance_payment_per_unit.unit,
        )

    @staticmethod
    def get_central_heating_settlement_output(
        central_heating_usage: UtilitySettlementInputWithMeters,
        central_heating_advance_payment_per_unit: AdvancePaymentPerUnit,
        central_heating_cost_per_unit: float,
        laf_factor: float,  # If LAF factors are not included in utilities settlement, LAF factor should be set to 1
    ) -> UtilitySettlementOutputWithMeters:
        return UtilitySettlementOutputWithMeters(
            utility_type=UtilityType.CO,
            actual_cost=round_number(
                central_heating_cost_per_unit
                * laf_factor
                * central_heating_usage.utility_usage_units
            ),
            advance_payment=central_heating_usage.advance_payment,
            advance_payment_per_unit=central_heating_advance_payment_per_unit.advance_payment_per_unit,
            meters_readings=central_heating_usage.meters_readings,
            actual_cost_per_unit=round_number(central_heating_cost_per_unit),
            unit=central_heating_advance_payment_per_unit.unit,
        )

    @classmethod
    def calculate_common_areas_cost_per_flat(
        cls,
        utilities_cost: UtilitiesCost,
        flats_settlement_input: list[FlatSettlementInput],
    ) -> float:
        """Common areas total cost is the cost of cold water that was not used by flats."""
        cold_water_utility = utilities_cost.utilities_with_meters_cost[UtilityType.ZW]

        remaining_cold_water = cls.get_remaining_cold_water_units(
            cold_water_utility.number_of_units,
            cold_water_usage_per_flat=[
                settlement_input.utilities_settlement_input_with_meters[UtilityType.ZW]
                for settlement_input in flats_settlement_input
            ],
            hot_water_usage_per_flat=[
                settlement_input.utilities_settlement_input_with_meters[UtilityType.CW]
                for settlement_input in flats_settlement_input
            ],
        )

        return round_number(
            remaining_cold_water
            * cold_water_utility.unit_cost
            / len(flats_settlement_input)
        )

    @staticmethod
    def get_remaining_cold_water_units(
        cold_water_total_used_units: float,
        cold_water_usage_per_flat: list[UtilitySettlementInputWithMeters],
        hot_water_usage_per_flat: list[UtilitySettlementInputWithMeters],
    ):
        """
        The difference between total number of used water units on the invoice
        and sum of used hot + cold water from all flats (based on meters readings) is considered
        as cold water used for common areas
        """
        return round_number(
            cold_water_total_used_units
            - sum(
                water_usage.utility_usage_units
                for water_usage in cold_water_usage_per_flat
            )
            - sum(
                water_usage.utility_usage_units
                for water_usage in hot_water_usage_per_flat
            )
        )
