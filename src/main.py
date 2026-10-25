
from src.distance import build_distance_matrix
from src.genetic_algorithm import (
    evaluate_fitness,
    initialize_population,
    select_elites,
    swap_mutation,
)


def main():
    cities = [
        (0, 0),  # A
        (2, 4),  # B
        (5, 2),  # C
        (6, 6),  # D
        (8, 3),  # E
    ]

    names = ["A", "B", "C", "D", "E"]
    matrix = build_distance_matrix(cities)

    population = initialize_population(
        len(cities), population_size=10, seed=42
    )

    best_route = select_elites(
        population, matrix, elite_count=1
    )[0]

    mutated_route = swap_mutation(
        best_route, mutation_rate=1.0, seed=42
    )

    elites = select_elites(
        population, matrix, elite_count=3
    )

    def show_route(route):
        route_names = [names[city] for city in route]
        route_names.append(route_names[0])
        return " -> ".join(route_names)

    print("=" * 45)
    print("PHASE 6: MUTATION AND ELITISM")
    print("=" * 45)

    print("\nBest original route:")
    print(show_route(best_route))
    print(f"Distance: {evaluate_fitness(best_route, matrix):.3f}")

    print("\nAfter swap mutation:")
    print(show_route(mutated_route))
    print(f"Distance: {evaluate_fitness(mutated_route, matrix):.3f}")

    print("\nTop 3 elite routes:")
    for index, route in enumerate(elites, start=1):
        print(
            f"{index}. {show_route(route)} | "
            f"Distance: {evaluate_fitness(route, matrix):.3f}"
        )

    print("\nOriginal best route preserved:", best_route in population)


if __name__ == "__main__":
    main()
