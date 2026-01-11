import pandas as pd

from datatypes import FlatId, FlatInformation


def parse_flats_information(data: pd.DataFrame) -> dict[FlatId, FlatInformation]:
    data = data.astype({"building_number": "str", "flat_number": "str"})
    flat_information_rows = data.to_dict(orient="records")

    result: dict[FlatId, FlatInformation] = {}
    for row in flat_information_rows:
        flat_info = FlatInformation.model_validate(row)
        result[flat_info.flat_id] = flat_info

    return result
