
from src.genetic_algorithm import (
    run_genetic_algorithm,
    validate_chromosome,
)
from src.baseline_solver import solve_baseline


def main():
    cities = [
        (0, 0),  # A
        (2, 4),  # B
        (5, 2),  # C
        (6, 6),  # D
        (8, 3),  # E
    ]

    names = ["A", "B", "C", "D", "E"]

    population_size = 50
    generations = 100

    print("=" * 50)
    print("TRAVELLING SALESPERSON PROBLEM SOLVER")
    print("GENETIC ALGORITHM")
    print("=" * 50)

    best_route, best_distance, history = run_genetic_algorithm(
        cities,
        population_size=population_size,
        generations=generations,
        crossover_rate=0.9,
        mutation_rate=0.1,
        tournament_size=3,
        elite_count=1,
        seed=42,
    )

    route_names = [names[city] for city in best_route]
    route_names.append(route_names[0])

    print(f"\nCities: {len(cities)}")
    print(f"Population size: {population_size}")
    print(f"Generations: {generations}")
    print("Algorithm: Genetic Algorithm")

    print("\nBest route found:")
    print(" -> ".join(route_names))
    print(f"Best distance: {best_distance:.3f}")
    print("Route valid:", validate_chromosome(best_route, len(cities)))

    print("\nConvergence:")
    print(f"Initial best distance: {history[0]:.3f}")
    print(f"Final best distance:   {history[-1]:.3f}")

    print("\nBest-so-far distance every 10 generations:")
    for generation in range(0, generations + 1, 10):
        print(
            f"Generation {generation:3}: "
            f"{history[generation]:.3f}"
        )

    # Compare with the random-search baseline.
    baseline_route, baseline_distance = solve_baseline(
        cities, trials=1000, seed=42
    )

    print("\nBaseline comparison:")
    print(f"Random search distance: {baseline_distance:.3f}")
    print(f"Genetic Algorithm:      {best_distance:.3f}")

    if best_distance < baseline_distance:
        print("GA found a shorter route in this experiment.")
    elif best_distance == baseline_distance:
        print("Both methods found routes with equal distance.")
    else:
        print("Random search found a shorter route in this experiment.")


if __name__ == "__main__":
    main()
