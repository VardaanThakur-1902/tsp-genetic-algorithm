
import csv
import random
import statistics
import time
from pathlib import Path

from src.baseline_solver import solve_baseline
from src.exact_solver import solve_exact
from src.genetic_algorithm import (
    run_genetic_algorithm,
    validate_chromosome,
)


def calculate_optimality_gap(
    distance: float,
    optimal_distance: float,
) -> float:
    """Calculate percentage gap from the exact optimum."""
    if optimal_distance < 0:
        raise ValueError("Optimal distance cannot be negative.")

    if distance < 0:
        raise ValueError("Route distance cannot be negative.")

    if optimal_distance == 0:
        if distance == 0:
            return 0.0
        raise ValueError(
            "A positive distance cannot be compared with a zero optimum."
        )

    return max(0.0, (distance - optimal_distance) / optimal_distance * 100)


def evaluate_solvers(
    cities: list[tuple[float, float]],
    repeats: int = 10,
    population_size: int = 50,
    generations: int = 100,
    baseline_trials: int = 1000,
    output_path: str = "results/evaluation_results.csv",
) -> list[dict]:
    """Compare GA and random search against the exact optimum."""
    if not cities:
        raise ValueError("At least one city is required.")

    if repeats < 1:
        raise ValueError("Repeats must be at least 1.")

    if population_size < 1 or generations < 0:
        raise ValueError("Invalid GA configuration.")

    if baseline_trials < 1:
        raise ValueError("Baseline trials must be at least 1.")

    # Exhaustive evaluation is only practical for small instances.
    if len(cities) > 10:
        raise ValueError(
            "Exact evaluation is limited to 10 cities in this module."
        )

    _, optimal_distance = solve_exact(cities)
    results = []

    for method in ("Random Search", "Genetic Algorithm"):
        distances = []
        gaps = []
        elapsed_times = []

        for repeat in range(repeats):
            seed = 1000 + repeat
            start = time.perf_counter()

            if method == "Random Search":
                _, distance = solve_baseline(
                    cities,
                    trials=baseline_trials,
                    seed=seed,
                )
            else:
                _, distance, _ = run_genetic_algorithm(
                    cities,
                    population_size=population_size,
                    generations=generations,
                    seed=seed,
                )

            elapsed = time.perf_counter() - start

            distances.append(distance)
            gaps.append(
                calculate_optimality_gap(distance, optimal_distance)
            )
            elapsed_times.append(elapsed)

        results.append({
            "method": method,
            "cities": len(cities),
            "repeats": repeats,
            "optimal_distance": optimal_distance,
            "mean_distance": statistics.mean(distances),
            "best_distance": min(distances),
            "worst_distance": max(distances),
            "mean_optimality_gap_percent": statistics.mean(gaps),
            "mean_runtime_seconds": statistics.mean(elapsed_times),
        })

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys()),
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"Evaluation results saved to: {path}")

    return results
