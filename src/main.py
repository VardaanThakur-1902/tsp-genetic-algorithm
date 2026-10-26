
from src.evaluation import evaluate_solvers
from src.exact_solver import solve_exact
from src.genetic_algorithm import run_genetic_algorithm, validate_chromosome
from src.distance import build_distance_matrix, calculate_route_distance


def main():
    cities = [
        (0, 0),
        (2, 4),
        (5, 2),
        (6, 6),
        (8, 3),
        (1, 7),
        (9, 8),
    ]

    print("=" * 60)
    print("PHASE 9: TSP SOLVER EVALUATION")
    print("=" * 60)

    optimal_route, optimal_distance = solve_exact(cities)

    print("\nExact solution:")
    print("Route:", optimal_route + [optimal_route[0]])
    print(f"Optimal distance: {optimal_distance:.3f}")

    ga_route, ga_distance, history = run_genetic_algorithm(
        cities,
        population_size=50,
        generations=100,
        crossover_rate=0.9,
        mutation_rate=0.1,
        tournament_size=3,
        elite_count=1,
        seed=42,
    )

    matrix = build_distance_matrix(cities)
    verified_distance = calculate_route_distance(ga_route, matrix)

    print("\nGenetic Algorithm validation:")
    print("Route:", ga_route + [ga_route[0]])
    print("Route valid:", validate_chromosome(ga_route, len(cities)))
    print(f"Reported distance: {ga_distance:.3f}")
    print(f"Verified distance: {verified_distance:.3f}")
    print(f"Optimality gap: {(ga_distance - optimal_distance) / optimal_distance * 100:.2f}%")
    print(f"Initial best distance: {history[0]:.3f}")
    print(f"Final best distance: {history[-1]:.3f}")

    results = evaluate_solvers(
        cities,
        repeats=10,
        population_size=50,
        generations=100,
        baseline_trials=1000,
        output_path="results/evaluation_results.csv",
    )

    print("\nRepeated-run comparison:")
    for result in results:
        print(f"\nMethod: {result['method']}")
        print(f"Mean distance: {result['mean_distance']:.3f}")
        print(f"Best distance: {result['best_distance']:.3f}")
        print(f"Worst distance: {result['worst_distance']:.3f}")
        print(
            "Mean optimality gap: "
            f"{result['mean_optimality_gap_percent']:.2f}%"
        )
        print(
            "Mean runtime: "
            f"{result['mean_runtime_seconds']:.6f} seconds"
        )


if __name__ == "__main__":
    main()
