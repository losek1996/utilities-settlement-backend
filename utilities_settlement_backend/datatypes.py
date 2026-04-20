from datetime import date
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, field_validator, model_validator

FlatId = str  # building_number + flat_number e.g. 9B_5


DEFAULT_LAF_FACTOR = 1.0


class FlatSettlementInput(BaseModel):
    flat_information: FlatInformation
    utilities_settlement_input_without_meters: dict[
        UtilityType, UtilitySettlementInputWithoutMeters
    ]
    utilities_settlement_input_with_meters: dict[
        UtilityType, UtilitySettlementInputWithMeters
    ]


class UtilitiesSettlementForFlat(BaseModel):
    flat_information: FlatInformation
    settlement_basic_information: UtilitiesSettlementBasicInformation
    utilities_settlement_without_advance_payment: dict[
        UtilityType, UtilitySettlementOutputWithoutAdvancePayment
    ]
    utilities_settlement_without_meters: dict[
        UtilityType, UtilitySettlementOutputWithoutMeters
    ]
    utilities_settlement_with_meters: dict[
        UtilityType, UtilitySettlementOutputWithMeters
    ]


class Flat(BaseModel):
    building_number: str
    flat_number: str

    @property
    def flat_id(self) -> FlatId:
        return f"{self.building_number}_{self.flat_number}"


class FlatInformation(Flat):
    flat_size: float  # in square meters
    laf_factor: float | None = None


class SettlementPeriod(BaseModel):
    start_date: date
    end_date: date


class UtilitiesSettlementBasicInformation(BaseModel):
    settlement_period_start_date: date
    settlement_period_end_date: date
    settlement_date: date
    housing_community_name: str
    street_name: str


class UtilitySettlementInputWithoutMeters(BaseModel):
    utility_type: UtilityType
    advance_payment: float


class UtilitySettlementInputWithMeters(UtilitySettlementInputWithoutMeters):
    meters_readings: list[
        MeterReadingInterval
    ]  # During settlement period meter can change

    @property
    def utility_usage_units(self) -> float:
        return sum(
            [
                meter_reading.current_value - meter_reading.previous_value
                for meter_reading in self.meters_readings
            ]
        )


class UtilitySettlementOutputWithoutAdvancePayment(BaseModel):
    utility_type: UtilityType
    actual_cost: float


class UtilitySettlementOutputWithoutMeters(
    UtilitySettlementOutputWithoutAdvancePayment
):
    advance_payment: float
    advance_payment_per_unit: float
    actual_cost_per_unit: float
    unit: str


class UtilitySettlementOutputWithMeters(UtilitySettlementOutputWithoutMeters):
    meters_readings: list[
        MeterReadingInterval
    ]  # During settlement period meter can change

    @property
    def utility_usage_units(self) -> float:
        return sum(
            [
                meter_reading.current_value - meter_reading.previous_value
                for meter_reading in self.meters_readings
            ]
        )


class UtilityType(StrEnum):
    ZW = "ZW"  # cold water
    CW = "CW"  # hot water
    CO = "CO"  # central heating
    CO_FIXED_FEE = "CO_FIXED_FEE"  # central heating fixed fee
    COMMON_AREAS_FEE = "COMMON_AREAS_FEE"

    """
    In some housing associations, there is a single bill that covers 
    both heating cold water for domestic use and water used for central heating.
    It is necessary to determine how the total cost is split between these two components.
    """
    HEAT_ENERGY = "HEAT_ENERGY"
    HEAT_ENERGY_FIXED_FEE = "HEAT_ENERGY_FIXED_FEE"


class MeterReadingInterval(BaseModel):
    meter_number: str
    current_date: date
    current_value: float

    previous_date: date  # If it is first meter reading, previous meter reading date must be set ARTIFICIALLY
    previous_value: float = 0

    @model_validator(mode="after")
    def check_if_meter_reading_is_increasing(self) -> Self:
        if self.current_value < self.previous_value:
            raise NonIncreasingMeterReadingValueError
        elif self.current_date < self.previous_date:
            raise NonIncreasingMeterReadingDateError
        return self


class MeterReadingStatus(StrEnum):
    OK = "OK"
    FAILURE = "FAILURE"


class MeterReading(Flat):
    utility_type: UtilityType
    meter_number: str
    date: date
    status: MeterReadingStatus
    value: float


class AdvancePayment(Flat):
    """
    How much is the full advance payment for a particular utility
    e.g. cold water for settlement period e.g. half-year.
    """

    utility_type: UtilityType
    advance_payment: float


class AdvancePaymentPerUnit(BaseModel):
    """Advance payment for a unit of a particular utility e.g. m^3 of cold water."""

    utility_type: UtilityType
    unit: str
    advance_payment_per_unit: float


class UtilityWithoutMetersCost(BaseModel):
    utility_type: UtilityType
    total_cost: float


class UtilityWithMetersCost(UtilityWithoutMetersCost):
    unit_type: str
    number_of_units: float

    @property
    def unit_cost(self) -> float:
        return self.total_cost / self.number_of_units

    @field_validator("number_of_units", mode="after")
    @classmethod
    def is_positive_number(cls, value: float | None) -> float | None:
        if value is not None and value < 0:
            raise NonPositiveUsageError
        return value


class UtilitiesCost(BaseModel):
    utilities_without_meters_cost: dict[UtilityType, UtilityWithoutMetersCost]
    utilities_with_meters_cost: dict[UtilityType, UtilityWithMetersCost]


class NonIncreasingMeterReadingValueError(Exception):
    pass


class NonIncreasingMeterReadingDateError(Exception):
    pass


class NonPositiveUsageError(Exception):
    """Usage units must be >= 0."""

    pass
