
import random

from src.distance import (
    build_distance_matrix,
    calculate_route_distance,
)


def solve_baseline(
    cities: list[tuple[float, float]],
    trials: int = 1000,
    seed: int | None = 42,
) -> tuple[list[int], float]:
    """
    Find a short TSP route using random search.

    Returns:
        best_route: The best route found.
        best_distance: Its total distance, including the return trip.
    """
    if not cities:
        raise ValueError("At least one city is required.")

    if trials < 1:
        raise ValueError("Trials must be at least 1.")

    if len(cities) == 1:
        return [0], 0.0

    rng = random.Random(seed)
    distance_matrix = build_distance_matrix(cities)

    # Keep city 0 fixed as the starting city.
    remaining_cities = list(range(1, len(cities)))

    best_route = None
    best_distance = float("inf")

    for _ in range(trials):
        # Generate a new random permutation.
        rng.shuffle(remaining_cities)
        route = [0] + remaining_cities.copy()

        distance = calculate_route_distance(
            route, distance_matrix
        )

        if distance < best_distance:
            best_route = route.copy()
            best_distance = distance

    return best_route, best_distance
