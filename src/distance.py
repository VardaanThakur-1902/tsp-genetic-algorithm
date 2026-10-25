
import math
from typing import Sequence

City = tuple[float, float]


def calculate_distance(city_a: City, city_b: City) -> float:
    """Calculate Euclidean distance between two cities."""
    x1, y1 = city_a
    x2, y2 = city_b

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def build_distance_matrix(
    cities: Sequence[City],
) -> list[list[float]]:
    """Build a matrix containing distances between every city."""
    n = len(cities)

    matrix = [
        [0.0 for _ in range(n)]
        for _ in range(n)
    ]

    for i in range(n):
        for j in range(i + 1, n):
            distance = calculate_distance(cities[i], cities[j])
            matrix[i][j] = distance
            matrix[j][i] = distance

    return matrix


def calculate_route_distance(
    route: Sequence[int],
    distance_matrix: Sequence[Sequence[float]],
) -> float:
    """Calculate a route's total distance, including the return trip."""
    if not route:
        return 0.0

    n = len(distance_matrix)

    if any(city < 0 or city >= n for city in route):
        raise ValueError("Route contains an invalid city index.")

    if len(set(route)) != len(route):
        raise ValueError("Route must not contain duplicate cities.")

    total_distance = 0.0

    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)]

        total_distance += distance_matrix[current_city][next_city]

    return total_distance
