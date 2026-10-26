
from pathlib import Path

import matplotlib

# Use a non-interactive backend for reliable PNG generation.
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def plot_route(
    cities: list[tuple[float, float]],
    route: list[int],
    output_path: str = "results/best_route.png",
) -> None:
    """Plot the cities and the best TSP route."""
    if not cities:
        raise ValueError("At least one city is required.")

    if sorted(route) != list(range(len(cities))):
        raise ValueError("Route must contain every city exactly once.")

    coordinates = [cities[index] for index in route]
    closed_route = coordinates + [coordinates[0]]

    x_values = [point[0] for point in closed_route]
    y_values = [point[1] for point in closed_route]

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(x_values, y_values, marker="o", label="Best route")

    for index, (x, y) in enumerate(cities):
        ax.annotate(
            f"City {index}",
            (x, y),
            xytext=(5, 5),
            textcoords="offset points",
        )

    ax.set_title("Travelling Salesperson Problem — Best Route")
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect("equal", adjustable="datalim")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)

    print(f"Route plot saved to: {path}")


def plot_convergence(
    history: list[float],
    output_path: str = "results/convergence.png",
) -> None:
    """Plot the best-so-far distance against generation."""
    if not history:
        raise ValueError("History cannot be empty.")

    if any(distance < 0 for distance in history):
        raise ValueError("Distances cannot be negative.")

    if any(
        history[i + 1] > history[i]
        for i in range(len(history) - 1)
    ):
        raise ValueError("Best-so-far history cannot increase.")

    generations = list(range(len(history)))

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(generations, history, marker=".", label="Best distance")

    ax.set_title("Genetic Algorithm Convergence")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best route distance")
    ax.grid(True, alpha=0.3)
    ax.legend()

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)

    print(f"Convergence plot saved to: {path}")



def plot_dual_route(
    cities,
    labels,
    route,
    output_path,
    title,
    metric_label,
    metric_value,
):
    """Plot a closed tour and label each city."""
    if len(cities) != len(labels):
        raise ValueError("Each city must have a corresponding label.")

    if not route or len(route) != len(cities):
        raise ValueError("Route must visit every city exactly once.")

    if sorted(route) != list(range(len(cities))):
        raise ValueError("Route must contain every city index exactly once.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    closed_route = route + [route[0]]
    route_x = [cities[i][0] for i in closed_route]
    route_y = [cities[i][1] for i in closed_route]

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.plot(
        route_x,
        route_y,
        marker="o",
        linewidth=1.8,
        label="Tour",
    )

    for i, (x, y) in enumerate(cities):
        ax.annotate(
            labels[i],
            (x, y),
            xytext=(6, 6),
            textcoords="offset points",
        )

    ax.scatter(
        [cities[route[0]][0]],
        [cities[route[0]][1]],
        marker="*",
        s=180,
        label="Starting city",
        zorder=3,
    )

    ax.set_title(f"{title}\n{metric_label}: {metric_value:.3f}")
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect("equal", adjustable="datalim")

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_dual_convergence(
    distance_history,
    cost_history,
    output_path,
):
    """Plot the GA convergence history for both objectives."""
    if not distance_history or not cost_history:
        raise ValueError("Convergence histories cannot be empty.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(
        range(len(distance_history)),
        distance_history,
        marker=".",
    )
    axes[0].set_title("Shortest-distance GA")
    axes[0].set_xlabel("Generation")
    axes[0].set_ylabel("Best distance")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(
        range(len(cost_history)),
        cost_history,
        marker=".",
    )
    axes[1].set_title("Minimum-cost GA")
    axes[1].set_xlabel("Generation")
    axes[1].set_ylabel("Best travel cost")
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_solution_comparison(
    shortest_result,
    cheapest_result,
    output_path,
):
    """Compare distance and cost for the two selected tours."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    categories = ["Total distance", "Total cost"]

    shortest_values = [
        shortest_result["total_distance"],
        shortest_result["total_cost"],
    ]
    cheapest_values = [
        cheapest_result["total_distance"],
        cheapest_result["total_cost"],
    ]

    positions = [0, 1]
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        [p - width / 2 for p in positions],
        shortest_values,
        width,
        label="Shortest-distance route",
    )
    ax.bar(
        [p + width / 2 for p in positions],
        cheapest_values,
        width,
        label="Minimum-cost route",
    )

    ax.set_xticks(positions)
    ax.set_xticklabels(categories)
    ax.set_ylabel("Value")
    ax.set_title("Distance and Cost Comparison")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
