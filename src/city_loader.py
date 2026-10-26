
import csv
from pathlib import Path


def load_cities(
    csv_path: str,
) -> tuple[list[tuple[float, float]], list[str]]:
    """Load city labels and coordinates from a CSV file."""
    path = Path(csv_path)

    if not path.is_file():
        raise FileNotFoundError(f"City CSV not found: {path}")

    cities = []
    labels = []

    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required_columns = {"city", "x", "y"}

        if not reader.fieldnames or not required_columns.issubset(
            reader.fieldnames
        ):
            raise ValueError(
                "CSV must contain city, x, and y columns."
            )

        for line_number, row in enumerate(reader, start=2):
            label = (row.get("city") or "").strip()

            if not label:
                raise ValueError(
                    f"Missing city label on line {line_number}."
                )

            try:
                x = float(row["x"])
                y = float(row["y"])
            except (TypeError, ValueError):
                raise ValueError(
                    f"Invalid coordinates on line {line_number}."
                ) from None

            if not (float("-inf") < x < float("inf")):
                raise ValueError(
                    f"Invalid X coordinate on line {line_number}."
                )

            if not (float("-inf") < y < float("inf")):
                raise ValueError(
                    f"Invalid Y coordinate on line {line_number}."
                )

            labels.append(label)
            cities.append((x, y))

    if not cities:
        raise ValueError("The CSV contains no cities.")

    if len(set(labels)) != len(labels):
        raise ValueError("City labels must be unique.")

    return cities, labels
