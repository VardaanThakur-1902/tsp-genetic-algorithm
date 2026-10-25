
from src.distance import build_distance_matrix
from src.baseline_solver import solve_baseline


def main():
    cities = [
        (0, 0),  # A
        (2, 4),  # B
        (5, 2),  # C
        (6, 6),  # D
        (8, 3),  # E
    ]

    city_names = ["A", "B", "C", "D", "E"]

    trials = 1000

    best_route, best_distance = solve_baseline(
        cities,
        trials=trials,
        seed=42,
    )

    route_names = [city_names[i] for i in best_route]
    route_names.append(route_names[0])

    print("=" * 45)
    print("BASELINE TSP SOLVER")
    print("=" * 45)
    print(f"Number of cities: {len(cities)}")
    print(f"Random trials: {trials}")
    print("Algorithm: Random Search")
    print("Best route:", " -> ".join(route_names))
    print(f"Best distance: {best_distance:.3f}")

    # Show the distances between consecutive cities.
    matrix = build_distance_matrix(cities)

    print("\nRoute breakdown:")
    for i in range(len(best_route)):
        current_city = best_route[i]
        next_city = best_route[(i + 1) % len(best_route)]

        distance = matrix[current_city][next_city]

        print(
            f"{city_names[current_city]} -> "
            f"{city_names[next_city]}: {distance:.3f}"
        )

    print(f"\nTotal distance: {best_distance:.3f}")


if __name__ == "__main__":
    main()
