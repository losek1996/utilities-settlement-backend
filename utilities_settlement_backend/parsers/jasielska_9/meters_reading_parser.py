import pandas as pd

from datatypes import FlatId, MeterReading


def parse_meter_readings(
    data: pd.DataFrame, meter_reading_date_str: str
) -> dict[FlatId, list[MeterReading]]:
    data = data.astype(
        {"building_number": "str", "flat_number": "str", "meter_number": "str"}
    )
    meter_reading_rows = data.to_dict(orient="records")

    result: dict[FlatId, list[MeterReading]] = {}
    for meter_reading_raw in meter_reading_rows:
        meter_reading_raw["date"] = meter_reading_date_str
        meter_reading = MeterReading.model_validate(meter_reading_raw)
        flat_id = meter_reading.flat_id

        if flat_id not in result:
            result[flat_id] = []

        result[flat_id].append(meter_reading)

    return result
