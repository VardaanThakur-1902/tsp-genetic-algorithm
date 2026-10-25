
from src.distance import build_distance_matrix
from src.genetic_algorithm import (
    initialize_population,
    evaluate_fitness,
    tournament_selection,
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

    print("=" * 50)
    print("PHASE 4: FITNESS AND TOURNAMENT SELECTION")
    print("=" * 50)

    print("\nPopulation fitness:")
    for index, chromosome in enumerate(population, start=1):
        distance = evaluate_fitness(chromosome, matrix)
        route = " -> ".join(names[c] for c in chromosome)
        route += f" -> {names[chromosome[0]]}"

        print(
            f"Chromosome {index:2}: "
            f"Distance = {distance:7.3f} | {route}"
        )

    best_route = min(
        population, key=lambda route: evaluate_fitness(route, matrix)
    )
    best_distance = evaluate_fitness(best_route, matrix)

    parent = tournament_selection(
        population,
        matrix,
        tournament_size=3,
        seed=123,
    )

    parent_distance = evaluate_fitness(parent, matrix)

    print("\nBest route in the full population:")
    print("Route:", " -> ".join(names[c] for c in best_route + [best_route[0]]))
    print(f"Distance: {best_distance:.3f}")

    print("\nSelected tournament parent:")
    print("Route:", " -> ".join(names[c] for c in parent + [parent[0]]))
    print(f"Distance: {parent_distance:.3f}")


if __name__ == "__main__":
    main()
