from abc import ABC, abstractmethod

from datatypes import (
    FlatSettlementInput,
    UtilitiesCost,
    UtilitiesSettlementForFlat,
    UtilitiesSettlementBasicInformation,
    UtilityType,
    AdvancePaymentPerUnit,
)


class ISettlementStrategy(ABC):
    @abstractmethod
    def generate_settlement(
        self,
        settlement_basic_information: UtilitiesSettlementBasicInformation,
        advance_payments_per_unit: dict[UtilityType, AdvancePaymentPerUnit],
        utilities_cost: UtilitiesCost,
        flats_settlement_input: list[FlatSettlementInput],
        include_laf_factor: bool,
    ) -> list[UtilitiesSettlementForFlat]:
        pass
