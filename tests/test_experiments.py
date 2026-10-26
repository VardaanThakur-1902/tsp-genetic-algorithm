
import csv
import pytest

from src.experiments import run_experiments


def test_experiments_return_expected_results(tmp_path):
    cities = [(0, 0), (3, 0), (3, 4)]
    output = tmp_path / "results.csv"

    results = run_experiments(
        cities,
        population_sizes=[5],
        mutation_rates=[0.1, 0.2],
        generations=3,
        repeats=2,
        output_path=str(output),
    )

    assert len(results) == 2
    assert output.exists()
    assert all(
        result["mean_best_distance"] >= 0
        for result in results
    )


def test_experiment_csv_contains_expected_columns(tmp_path):
    output = tmp_path / "results.csv"

    run_experiments(
        [(0, 0), (1, 0), (1, 1)],
        population_sizes=[5],
        mutation_rates=[0.1],
        generations=2,
        repeats=1,
        output_path=str(output),
    )

    with output.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        assert "mean_best_distance" in reader.fieldnames
        assert "population_size" in reader.fieldnames


def test_invalid_experiment_configuration():
    with pytest.raises(ValueError):
        run_experiments(
            [(0, 0), (1, 0)],
            population_sizes=[],
            mutation_rates=[0.1],
        )

    with pytest.raises(ValueError):
        run_experiments(
            [(0, 0), (1, 0)],
            population_sizes=[5],
            mutation_rates=[1.5],
        )
