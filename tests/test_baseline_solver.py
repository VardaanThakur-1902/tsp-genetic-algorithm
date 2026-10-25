
import pytest

from src.baseline_solver import solve_baseline


def test_solver_returns_every_city_once():
    cities = [(0, 0), (2, 4), (5, 2), (6, 6), (8, 3)]

    route, distance = solve_baseline(cities, trials=100, seed=42)

    assert len(route) == len(cities)
    assert sorted(route) == list(range(len(cities)))
    assert route[0] == 0
    assert distance > 0


def test_solver_is_reproducible():
    cities = [(0, 0), (2, 4), (5, 2), (6, 6), (8, 3)]

    result1 = solve_baseline(cities, trials=100, seed=42)
    result2 = solve_baseline(cities, trials=100, seed=42)

    assert result1 == result2


def test_single_city():
    route, distance = solve_baseline([(5, 5)])

    assert route == [0]
    assert distance == 0.0


def test_empty_cities_rejected():
    with pytest.raises(ValueError):
        solve_baseline([])


def test_zero_trials_rejected():
    with pytest.raises(ValueError):
        solve_baseline([(0, 0), (1, 1)], trials=0)


def test_more_trials_cannot_worsen_best_result():
    cities = [(0, 0), (2, 4), (5, 2), (6, 6), (8, 3)]

    _, short_result = solve_baseline(
        cities, trials=100, seed=42
    )
    _, long_result = solve_baseline(
        cities, trials=1000, seed=42
    )

    assert long_result <= short_result
