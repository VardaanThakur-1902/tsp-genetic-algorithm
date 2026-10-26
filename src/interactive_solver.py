
import json
import time
from pathlib import Path

from src.distance import build_distance_matrix
from src.genetic_algorithm import (
    evaluate_fitness,
    run_genetic_algorithm_for_matrix,
)
from src.interactive_input import collect_problem_input

from src.visualization import (
    plot_dual_route,
    plot_dual_convergence,
    plot_solution_comparison,
)


def main():
    try:
        cities, labels, cost_matrix = collect_problem_input()
    except ValueError as error:
        print(f"\nInput error: {error}")
        return

    distance_matrix = build_distance_matrix(cities)

    # Shared GA configuration for a fair comparison.
    config = {
        "population_size": 100,
        "generations": 300,
        "crossover_rate": 0.9,
        "mutation_rate": 0.1,
        "tournament_size": 3,
        "elite_count": 1,
        "seed": 42,
    }

    print("\nFinding the shortest-distance route...")
    start = time.perf_counter()

    distance_route, _, distance_history = (
        run_genetic_algorithm_for_matrix(
            distance_matrix, **config
        )
    )

    distance_runtime = time.perf_counter() - start

    print("Finding the minimum-cost route...")
    start = time.perf_counter()

    
    cost_config = {**config, "seed": 43}

    cost_route, _, cost_history = run_genetic_algorithm_for_matrix(
        cost_matrix,
        **cost_config,
    )


    cost_runtime = time.perf_counter() - start

    def route_details(route):
        closed_route = route + [route[0]]
        route_names = [labels[index] for index in closed_route]

        total_distance = evaluate_fitness(route, distance_matrix)
        total_cost = evaluate_fitness(route, cost_matrix)

        return {
            "route_indices": route,
            "route": route_names,
            "total_distance": total_distance,
            "total_cost": total_cost,
        }

    shortest_result = route_details(distance_route)
    cheapest_result = route_details(cost_route)

    
    # Save the shortest-distance route visualization.
    plot_dual_route(
        cities=cities,
        labels=labels,
        route=distance_route,
        output_path="results/shortest_distance_route.png",
        title="Shortest-Distance Route",
        metric_label="Total distance",
        metric_value=shortest_result["total_distance"],
    )

    # Save the minimum-cost route visualization.
    plot_dual_route(
        cities=cities,
        labels=labels,
        route=cost_route,
        output_path="results/minimum_cost_route.png",
        title="Minimum-Cost Route",
        metric_label="Total cost",
        metric_value=cheapest_result["total_cost"],
    )

    # Save both GA convergence histories.
    plot_dual_convergence(
        distance_history=distance_history,
        cost_history=cost_history,
        output_path="results/dual_convergence.png",
    )

    # Compare distance and cost for the selected tours.
    plot_solution_comparison(
        shortest_result=shortest_result,
        cheapest_result=cheapest_result,
        output_path="results/solution_comparison.png",
    )

    print("\nVisualization files saved:")
    print(" - results/shortest_distance_route.png")
    print(" - results/minimum_cost_route.png")
    print(" - results/dual_convergence.png")
    print(" - results/solution_comparison.png")


    print("\n" + "=" * 60)
    print("TRAVELLING SALESPERSON PROBLEM SOLVER")
    print("=" * 60)

    print("\nSHORTEST-DISTANCE ROUTE")
    print(" -> ".join(shortest_result["route"]))
    print(f"Total distance: {shortest_result['total_distance']:.3f}")
    print(f"Total travel cost: {shortest_result['total_cost']:.2f}")
    print(f"Runtime: {distance_runtime:.6f} seconds")

    print("\nMINIMUM-COST ROUTE")
    print(" -> ".join(cheapest_result["route"]))
    print(f"Total distance: {cheapest_result['total_distance']:.3f}")
    print(f"Total travel cost: {cheapest_result['total_cost']:.2f}")
    print(f"Runtime: {cost_runtime:.6f} seconds")

    results = {
        "cities": [
            {"name": labels[i], "x": cities[i][0], "y": cities[i][1]}
            for i in range(len(cities))
        ],
        "cost_matrix": cost_matrix,
        "configuration": config,
        "shortest_distance_solution": {
            **shortest_result,
            "runtime_seconds": distance_runtime,
            "convergence_history": distance_history,
        },
        "minimum_cost_solution": {
            **cheapest_result,
            "runtime_seconds": cost_runtime,
            "convergence_history": cost_history,
        },
    }

    output_path = Path("results/dual_optimization_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
