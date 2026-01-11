import pandas as pd

from datatypes import AdvancePayment, AdvancePaymentPerUnit, FlatId, UtilityType


def parse_advance_payments(
    data: pd.DataFrame,
) -> dict[FlatId, dict[UtilityType, AdvancePayment]]:
    data = data.astype({"building_number": "str", "flat_number": "str"})
    advance_payment_rows = data.to_dict(orient="records")

    result: dict[FlatId, dict[UtilityType, AdvancePayment]] = {}
    for row in advance_payment_rows:
        advance_payment = AdvancePayment.model_validate(row)
        flat_id = advance_payment.flat_id

        if flat_id not in result:
            result[flat_id] = {}

        result[flat_id][advance_payment.utility_type] = advance_payment

    return result


def parse_advance_payments_per_unit(
    data: pd.DataFrame,
) -> dict[UtilityType, AdvancePaymentPerUnit]:
    advance_payment_per_unit_rows = data.to_dict(orient="records")

    result: dict[UtilityType, AdvancePaymentPerUnit] = {}
    for row in advance_payment_per_unit_rows:
        advance_payment_per_unit = AdvancePaymentPerUnit.model_validate(row)
        result[advance_payment_per_unit.utility_type] = advance_payment_per_unit

    return result
