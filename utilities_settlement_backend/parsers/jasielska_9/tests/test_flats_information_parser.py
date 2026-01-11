from os import path

from csv_reader import read_csv_file
from parsers.jasielska_9.flats_information_parser import parse_flats_information

DATA_DIR = path.join(
    path.dirname(path.realpath(__file__)),
    "data",
)


def test_read_flat_information():
    df = read_csv_file(path.join(DATA_DIR, "flats_information.csv"))
    result = parse_flats_information(df)

    assert len(result) == 5

    flat_9_1 = result["9_1"]
    assert flat_9_1.building_number == "9"
    assert flat_9_1.flat_number == "1"
    assert flat_9_1.flat_size == 30.0
    assert flat_9_1.laf_factor == 0.7
    assert flat_9_1.flat_id == "9_1"

    flat_9_5 = result["9_5"]
    assert flat_9_5.building_number == "9"
    assert flat_9_5.flat_number == "5"
    assert flat_9_5.flat_size == 50.0
    assert flat_9_5.laf_factor == 0.5
    assert flat_9_5.flat_id == "9_5"
