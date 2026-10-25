
from src.distance import (
    build_distance_matrix,
    calculate_distance,
    calculate_route_distance,
)


def main():
    # Coordinates for five cities: A, B, C, D, E
    cities = [
        (0, 0),  # A
        (2, 4),  # B
        (5, 2),  # C
        (6, 6),  # D
        (8, 3),  # E
    ]

    city_names = ["A", "B", "C", "D", "E"]

    # Calculate distance between two cities
    distance_ab = calculate_distance(cities[0], cities[1])
    print(f"Distance A to B: {distance_ab:.3f}")

    # Create distance matrix
    matrix = build_distance_matrix(cities)

    print("\nDistance Matrix:")
    print("    " + "  ".join(city_names))

    for i, row in enumerate(matrix):
        formatted_row = "  ".join(f"{d:6.2f}" for d in row)
        print(f"{city_names[i]}  {formatted_row}")

    # Test one possible route
    route = [0, 1, 2, 3, 4]
    total = calculate_route_distance(route, matrix)

    route_names = [city_names[i] for i in route]
    route_names.append(route_names[0])

    print("\nExample route:", " -> ".join(route_names))
    print(f"Total route distance: {total:.3f}")


if __name__ == "__main__":
    main()
