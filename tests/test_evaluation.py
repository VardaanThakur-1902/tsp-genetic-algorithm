
import csv
import pytest

from src.exact_solver import solve_exact
from src.evaluation import (
    calculate_optimality_gap,
    evaluate_solvers,
)
from src.distance import build_distance_matrix
from src.genetic_algorithm import (
    run_genetic_algorithm,
    validate_chromosome,
)


def test_exact_solver_finds_triangle_optimum():
    cities = [(0, 0), (3, 0), (3, 4)]

    route, distance = solve_exact(cities)

    assert validate_chromosome(route, len(cities))
    assert distance == pytest.approx(12.0)


def test_exact_solver_single_city():
    route, distance = solve_exact([(5, 5)])

    assert route == [0]
    assert distance == 0.0


def test_exact_solver_rejects_empty_input():
    with pytest.raises(ValueError):
        solve_exact([])


def test_exact_solver_is_no_worse_than_any_ga_route():
    cities = [(0, 0), (2, 4), (5, 2), (6, 6), (8, 3)]

    _, optimal_distance = solve_exact(cities)
    _, ga_distance, _ = run_genetic_algorithm(
        cities, population_size=10, generations=10, seed=42
    )

    assert optimal_distance <= ga_distance + 1e-9


def test_optimality_gap_for_optimal_solution():
    assert calculate_optimality_gap(10.0, 10.0) == pytest.approx(0.0)


def test_optimality_gap_for_suboptimal_solution():
    assert calculate_optimality_gap(11.0, 10.0) == pytest.approx(10.0)


def test_optimality_gap_handles_zero_optimum():
    assert calculate_optimality_gap(0.0, 0.0) == 0.0

    with pytest.raises(ValueError):
        calculate_optimality_gap(1.0, 0.0)


def test_evaluation_creates_csv(tmp_path):
    cities = [(0, 0), (3, 0), (3, 4)]
    output = tmp_path / "evaluation.csv"

    results = evaluate_solvers(
        cities,
        repeats=2,
        population_size=5,
        generations=3,
        baseline_trials=10,
        output_path=str(output),
    )

    assert len(results) == 2
    assert output.exists()

    with output.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 2
    assert {row["method"] for row in rows} == {
        "Random Search",
        "Genetic Algorithm",
    }


def test_evaluation_rejects_too_many_cities():
    cities = [(float(i), 0.0) for i in range(11)]

    with pytest.raises(ValueError):
        evaluate_solvers(cities)
