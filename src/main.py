
from src.genetic_algorithm import (
    initialize_population,
    validate_chromosome,
)
from src.distance import (
    build_distance_matrix,
    calculate_route_distance,
)


def main():
    cities = [
        (0, 0),  # A
        (2, 4),  # B
        (5, 2),  # C
        (6, 6),  # D
        (8, 3),  # E
    ]

    city_names = ["A", "B", "C", "D", "E"]
    population_size = 10

    population = initialize_population(
        number_of_cities=len(cities),
        population_size=population_size,
        seed=42,
    )

    distance_matrix = build_distance_matrix(cities)

    print("=" * 45)
    print("GENETIC ALGORITHM - INITIAL POPULATION")
    print("=" * 45)
    print(f"Number of cities: {len(cities)}")
    print(f"Population size: {len(population)}")

    for i, chromosome in enumerate(population, start=1):
        distance = calculate_route_distance(
            chromosome, distance_matrix
        )

        route_names = [city_names[c] for c in chromosome]
        route_names.append(route_names[0])

        valid = validate_chromosome(chromosome, len(cities))

        print(f"\nChromosome {i}:")
        print("Route:", " -> ".join(route_names))
        print(f"Distance: {distance:.3f}")
        print(f"Valid: {valid}")


if __name__ == "__main__":
    main()
