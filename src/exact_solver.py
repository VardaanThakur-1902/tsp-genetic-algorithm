
from itertools import permutations
from collections.abc import Sequence

from src.distance import (
    build_distance_matrix,
    calculate_route_distance,
)


def solve_exact(
    cities: Sequence[tuple[float, float]],
) -> tuple[list[int], float]:
    """Find the exact optimal TSP tour by exhaustive enumeration.

    Intended for small instances because runtime grows factorially.
    City 0 remains fixed to avoid duplicate rotations.
    """
    if not cities:
        raise ValueError("At least one city is required.")

    if len(cities) == 1:
        return [0], 0.0

    distance_matrix = build_distance_matrix(cities)

    best_route = None
    best_distance = float("inf")

    for ordering in permutations(range(1, len(cities))):
        route = [0, *ordering]

        distance = calculate_route_distance(
            route, distance_matrix
        )

        if distance < best_distance:
            best_route = route
            best_distance = distance

    return best_route, best_distance
