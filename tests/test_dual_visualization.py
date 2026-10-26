
from src.visualization import (
    plot_dual_route,
    plot_dual_convergence,
    plot_solution_comparison,
)


def test_dual_route_plot_is_created(tmp_path):
    cities = [(0, 0), (3, 0), (0, 4)]
    labels = ["A", "B", "C"]
    route = [0, 1, 2]
    output = tmp_path / "route.png"

    plot_dual_route(
        cities,
        labels,
        route,
        output,
        "Shortest Route",
        "Distance",
        12.0,
    )

    assert output.exists()
    assert output.stat().st_size > 0


def test_dual_convergence_plot_is_created(tmp_path):
    output = tmp_path / "convergence.png"

    plot_dual_convergence(
        [12.0, 10.0, 9.0, 9.0],
        [500.0, 400.0, 350.0, 350.0],
        output,
    )

    assert output.exists()
    assert output.stat().st_size > 0


def test_solution_comparison_plot_is_created(tmp_path):
    shortest = {
        "total_distance": 10.0,
        "total_cost": 500.0,
    }
    cheapest = {
        "total_distance": 15.0,
        "total_cost": 350.0,
    }
    output = tmp_path / "comparison.png"

    plot_solution_comparison(shortest, cheapest, output)

    assert output.exists()
    assert output.stat().st_size > 0


def test_dual_route_rejects_invalid_route(tmp_path):
    output = tmp_path / "invalid.png"

    try:
        plot_dual_route(
            [(0, 0), (1, 1), (2, 2)],
            ["A", "B", "C"],
            [0, 1],
            output,
            "Invalid route",
            "Distance",
            3.0,
        )
        assert False, "Expected ValueError"
    except ValueError:
        pass

    assert not output.exists()
