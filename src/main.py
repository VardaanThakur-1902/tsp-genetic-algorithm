
from src.genetic_algorithm import run_genetic_algorithm
from src.visualization import plot_route, plot_convergence
from src.experiments import run_experiments


def main():
    cities = [
        (0, 0),
        (2, 4),
        (5, 2),
        (6, 6),
        (8, 3),
        (1, 7),
        (9, 8),
        (4, 9),
    ]

    best_route, best_distance, history = run_genetic_algorithm(
        cities,
        population_size=50,
        generations=100,
        crossover_rate=0.9,
        mutation_rate=0.1,
        tournament_size=3,
        elite_count=1,
        seed=42,
    )

    print("=" * 50)
    print("TSP GENETIC ALGORITHM — PHASE 8")
    print("=" * 50)
    print("Best route:", best_route + [best_route[0]])
    print(f"Best distance: {best_distance:.3f}")
    print(f"Initial best distance: {history[0]:.3f}")
    print(f"Final best distance: {history[-1]:.3f}")

    plot_route(cities, best_route)
    plot_convergence(history)

    results = run_experiments(
        cities,
        population_sizes=[20, 50, 100],
        mutation_rates=[0.05, 0.1, 0.2],
        generations=100,
        repeats=3,
    )

    print("\nExperiment summary:")
    for result in results:
        print(
            f"Population={result['population_size']:3}, "
            f"Mutation={result['mutation_rate']:.2f}, "
            f"Mean distance={result['mean_best_distance']:.3f}"
        )


if __name__ == "__main__":
    main()
