
import math


def collect_problem_input():
    """Collect city coordinates and pairwise travel costs from the user."""

    try:
        number_of_cities = int(input("Enter the number of cities: "))
    except ValueError:
        raise ValueError("Number of cities must be an integer.") from None

    if number_of_cities < 2:
        raise ValueError("Enter at least 2 cities.")

    cities = []
    labels = []
    seen_labels = set()

    print("\nEnter each city's details.")

    for i in range(number_of_cities):
        name = input(f"\nName of city {i + 1}: ").strip()

        if not name:
            raise ValueError("City names cannot be empty.")
        if name in seen_labels:
            raise ValueError(f"Duplicate city name: {name}")

        try:
            x = float(input(f"X coordinate of {name}: "))
            y = float(input(f"Y coordinate of {name}: "))
        except ValueError:
            raise ValueError("Coordinates must be numeric.") from None

        if not math.isfinite(x) or not math.isfinite(y):
            raise ValueError("Coordinates must be finite numbers.")

        labels.append(name)
        cities.append((x, y))
        seen_labels.add(name)

    cost_matrix = [
        [0.0 for _ in range(number_of_cities)]
        for _ in range(number_of_cities)
    ]

    print("\nEnter travel costs for each pair of cities.")
    print("Costs are bidirectional and must be non-negative.")

    for i in range(number_of_cities):
        for j in range(i + 1, number_of_cities):
            prompt = f"Cost from {labels[i]} to {labels[j]}: "

            try:
                cost = float(input(prompt))
            except ValueError:
                raise ValueError("Travel costs must be numeric.") from None

            if not math.isfinite(cost) or cost < 0:
                raise ValueError(
                    "Travel costs must be finite and non-negative."
                )

            cost_matrix[i][j] = cost
            cost_matrix[j][i] = cost

    return cities, labels, cost_matrix
