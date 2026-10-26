
import pytest

from src.city_loader import load_cities


def test_load_valid_city_csv(tmp_path):
    path = tmp_path / "cities.csv"
    path.write_text(
        "city,x,y\nA,0,0\nB,3,4\n",
        encoding="utf-8",
    )

    cities, labels = load_cities(str(path))

    assert cities == [(0.0, 0.0), (3.0, 4.0)]
    assert labels == ["A", "B"]


def test_missing_csv_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_cities(str(tmp_path / "missing.csv"))


def test_missing_columns_rejected(tmp_path):
    path = tmp_path / "cities.csv"
    path.write_text("name,latitude,longitude\nA,0,0\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_cities(str(path))


def test_invalid_coordinates_rejected(tmp_path):
    path = tmp_path / "cities.csv"
    path.write_text("city,x,y\nA,invalid,0\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_cities(str(path))


def test_duplicate_labels_rejected(tmp_path):
    path = tmp_path / "cities.csv"
    path.write_text("city,x,y\nA,0,0\nA,1,1\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_cities(str(path))


def test_empty_csv_data_rejected(tmp_path):
    path = tmp_path / "cities.csv"
    path.write_text("city,x,y\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_cities(str(path))
