
import argparse
import time

from src.baseline_solver import solve_baseline
from src.city_loader import load_cities
from src.genetic_algorithm import run_genetic_algorithm
from src.result_exporter import save_result


def build_parser():
    parser = argparse.ArgumentParser(
        description="Travelling Salesperson Problem Solver"
    )

    parser.add_argument(
        "--cities",
        default="data/cities.csv",
        help="Path to city CSV (city,x,y).",
    )

    parser.add_argument(
        "--algorithm",
        choices=["ga", "baseline"],
        default="ga",
        help="Solver to use.",
    )

    parser.add_argument("--population-size", type=int, default=50)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--crossover-rate", type=float, default=0.9)
    parser.add_argument("--mutation-rate", type=float, default=0.1)
    parser.add_argument("--tournament-size", type=int, default=3)
    parser.add_argument("--elite-count", type=int, default=1)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        default="results/run_result.json",
        help="Path for the JSON result.",
    )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        cities, labels = load_cities(args.cities)

        if args.algorithm == "ga":
            if args.population_size < 1:
                parser.error("--population-size must be positive.")
            if args.generations < 0:
                parser.error("--generations cannot be negative.")
            if not 0 <= args.crossover_rate <= 1:
                parser.error("--crossover-rate must be between 0 and 1.")
            if not 0 <= args.mutation_rate <= 1:
                parser.error("--mutation-rate must be between 0 and 1.")
            if not 1 <= args.tournament_size <= args.population_size:
                parser.error(
                    "--tournament-size must be between 1 and "
                    "--population-size."
                )
            if not 1 <= args.elite_count <= args.population_size:
                parser.error(
                    "--elite-count must be between 1 and "
                    "--population-size."
                )

        if args.algorithm == "baseline" and args.trials < 1:
            parser.error("--trials must be positive.")

        start = time.perf_counter()

        if args.algorithm == "ga":
            route, distance, history = run_genetic_algorithm(
                cities,
                population_size=args.population_size,
                generations=args.generations,
                crossover_rate=args.crossover_rate,
                mutation_rate=args.mutation_rate,
                tournament_size=args.tournament_size,
                elite_count=args.elite_count,
                seed=args.seed,
            )

            configuration = {
                "population_size": args.population_size,
                "generations": args.generations,
                "crossover_rate": args.crossover_rate,
                "mutation_rate": args.mutation_rate,
                "tournament_size": args.tournament_size,
                "elite_count": args.elite_count,
                "seed": args.seed,
            }

        else:
            route, distance = solve_baseline(
                cities,
                trials=args.trials,
                seed=args.seed,
            )
            history = []

            configuration = {
                "trials": args.trials,
                "seed": args.seed,
            }

        runtime = time.perf_counter() - start

        # Append the starting city to show the closed tour.
        closed_route = route + [route[0]]
        route_labels = [labels[index] for index in closed_route]

        print("\n" + "=" * 55)
        print("TRAVELLING SALESPERSON PROBLEM SOLVER")
        print("=" * 55)
        print(f"Algorithm: {args.algorithm}")
        print(f"Number of cities: {len(cities)}")
        print("Best route:", " -> ".join(route_labels))
        print(f"Total distance: {distance:.3f}")
        print(f"Runtime: {runtime:.6f} seconds")

        if history:
            print(f"Initial best distance: {history[0]:.3f}")
            print(f"Final best distance: {history[-1]:.3f}")

        save_result(
            output_path=args.output,
            algorithm=args.algorithm,
            route=route,
            route_labels=route_labels,
            distance=distance,
            runtime_seconds=runtime,
            configuration=configuration,
        )

    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
