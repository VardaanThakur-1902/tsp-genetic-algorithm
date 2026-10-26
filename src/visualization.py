
from pathlib import Path
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
