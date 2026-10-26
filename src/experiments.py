
import csv
from pathlib import Path

from src.genetic_algorithm import run_genetic_algorithm


def run_experiments(
    cities: list[tuple[float, float]],
    population_sizes: list[int],
    mutation_rates: list[float],
    generations: int = 100,
    repeats: int = 3,
    output_path: str = "results/experiment_results.csv",
) -> list[dict]:
    """Compare GA configurations across multiple random seeds."""
    if not population_sizes or not mutation_rates:
        raise ValueError("Experiment configurations cannot be empty.")

    if any(size < 1 for size in population_sizes):
        raise ValueError("Population sizes must be positive.")

    if any(not 0.0 <= rate <= 1.0 for rate in mutation_rates):
        raise ValueError("Mutation rates must be between 0 and 1.")

    if generations < 0 or repeats < 1:
        raise ValueError("Generations must be nonnegative and repeats positive.")

    results = []

    for population_size in population_sizes:
        for mutation_rate in mutation_rates:
            distances = []

            for repeat in range(repeats):
                seed = 1000 + repeat

                _, best_distance, _ = run_genetic_algorithm(
                    cities,
                    population_size=population_size,
                    generations=generations,
                    mutation_rate=mutation_rate,
                    seed=seed,
                )

                distances.append(best_distance)

            results.append({
                "population_size": population_size,
                "mutation_rate": mutation_rate,
                "generations": generations,
                "repeats": repeats,
                "mean_best_distance": sum(distances) / len(distances),
                "best_distance": min(distances),
                "worst_distance": max(distances),
            })

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Experiment results saved to: {path}")

    return results
