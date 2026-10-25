
import pytest

from src.distance import (
    calculate_distance,
    build_distance_matrix,
    calculate_route_distance,
)


def test_distance_between_two_cities():
    assert calculate_distance((0, 0), (3, 4)) == pytest.approx(5.0)


def test_distance_to_same_city():
    assert calculate_distance((2, 3), (2, 3)) == 0.0


def test_distance_matrix_is_symmetric():
    cities = [(0, 0), (3, 4), (6, 0)]
    matrix = build_distance_matrix(cities)

    assert matrix[0][1] == pytest.approx(matrix[1][0])
    assert matrix[0][2] == pytest.approx(matrix[2][0])


def test_distance_matrix_diagonal_is_zero():
    cities = [(0, 0), (3, 4), (6, 0)]
    matrix = build_distance_matrix(cities)

    for i in range(len(cities)):
        assert matrix[i][i] == 0.0


def test_route_includes_return_to_start():
    cities = [(0, 0), (3, 0), (3, 4)]
    matrix = build_distance_matrix(cities)

    distance = calculate_route_distance([0, 1, 2], matrix)

    # 3 + 4 + 5 = 12
    assert distance == pytest.approx(12.0)


def test_duplicate_cities_are_rejected():
    matrix = build_distance_matrix([(0, 0), (1, 0), (2, 0)])

    with pytest.raises(ValueError):
        calculate_route_distance([0, 1, 1], matrix)
