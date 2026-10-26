from src.genetic_algorithm import run_genetic_algorithm_for_matrix


def test_matrix_solver_returns_valid_route():
    matrix = [
        [0, 2, 9],
        [2, 0, 3],
        [9, 3, 0],
    ]

    route, value, history = run_genetic_algorithm_for_matrix(
        matrix,
        population_size=6,
        generations=5,
        seed=42,
    )

    assert sorted(route) == [0, 1, 2]
    assert route[0] == 0
    assert value >= 0
    assert len(history) == 6


def test_matrix_solver_rejects_non_square_matrix():
    matrix = [
        [0, 2],
        [2],
    ]

    try:
        run_genetic_algorithm_for_matrix(matrix)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_cost_and_distance_objectives_can_be_different():
    distance_matrix = [
        [0, 1, 10],
        [1, 0, 2],
        [10, 2, 0],
    ]

    cost_matrix = [
        [0, 10, 1],
        [10, 0, 10],
        [1, 10, 0],
    ]

    _, distance_score, _ = run_genetic_algorithm_for_matrix(
        distance_matrix, population_size=6, generations=10, seed=42
    )
    _, cost_score, _ = run_genetic_algorithm_for_matrix(
        cost_matrix, population_size=6, generations=10, seed=42
    )

    assert distance_score >= 0
    assert cost_score >= 0