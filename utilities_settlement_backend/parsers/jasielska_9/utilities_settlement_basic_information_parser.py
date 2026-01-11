import pandas as pd

from datatypes import UtilitiesSettlementBasicInformation


def parse_utilities_settlement_basic_information(
    data: pd.DataFrame,
) -> UtilitiesSettlementBasicInformation:
    utilities_cost_rows = data.to_dict(orient="records")
    basic_information = UtilitiesSettlementBasicInformation.model_validate(
        utilities_cost_rows[0]
    )
    return basic_information
