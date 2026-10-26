
import json

from src.result_exporter import save_result


def test_save_result_creates_json(tmp_path):
    output = tmp_path / "nested" / "result.json"

    save_result(
        output_path=str(output),
        algorithm="ga",
        route=[0, 1, 2],
        route_labels=["A", "B", "C", "A"],
        distance=12.0,
        runtime_seconds=0.01,
        configuration={"population_size": 20, "seed": 42},
    )

    assert output.exists()

    with output.open(encoding="utf-8") as file:
        data = json.load(file)

    assert data["algorithm"] == "ga"
    assert data["route_indices"] == [0, 1, 2]
    assert data["route_labels"] == ["A", "B", "C", "A"]
    assert data["distance"] == 12.0
    assert data["configuration"]["seed"] == 42
