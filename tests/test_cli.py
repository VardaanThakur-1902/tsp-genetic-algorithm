
import json

from src.main import main


def test_cli_runs_ga_and_saves_result(tmp_path):
    cities_file = tmp_path / "cities.csv"
    cities_file.write_text(
        "city,x,y\nA,0,0\nB,3,0\nC,3,4\n",
        encoding="utf-8",
    )

    output = tmp_path / "result.json"

    main([
        "--cities", str(cities_file),
        "--algorithm", "ga",
        "--population-size", "5",
        "--generations", "3",
        "--seed", "42",
        "--output", str(output),
    ])

    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["algorithm"] == "ga"
    assert len(data["route_indices"]) == 3
    assert data["distance"] > 0


def test_cli_runs_baseline_and_saves_result(tmp_path):
    cities_file = tmp_path / "cities.csv"
    cities_file.write_text(
        "city,x,y\nA,0,0\nB,3,0\nC,3,4\n",
        encoding="utf-8",
    )

    output = tmp_path / "baseline.json"

    main([
        "--cities", str(cities_file),
        "--algorithm", "baseline",
        "--trials", "10",
        "--seed", "42",
        "--output", str(output),
    ])

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["algorithm"] == "baseline"
    assert data["configuration"]["trials"] == 10
