
import pytest

from src.visualization import plot_route, plot_convergence


def test_route_plot_is_created(tmp_path):
    cities = [(0, 0), (3, 0), (3, 4)]
    route = [0, 1, 2]
    output = tmp_path / "route.png"

    plot_route(cities, route, str(output))

    assert output.exists()
    assert output.stat().st_size > 0


def test_convergence_plot_is_created(tmp_path):
    history = [12.0, 10.0, 9.0, 9.0]
    output = tmp_path / "convergence.png"

    plot_convergence(history, str(output))

    assert output.exists()
    assert output.stat().st_size > 0


def test_route_plot_rejects_invalid_route(tmp_path):
    with pytest.raises(ValueError):
        plot_route(
            [(0, 0), (1, 0), (2, 0)],
            [0, 1, 1],
            str(tmp_path / "invalid.png"),
        )


def test_convergence_plot_rejects_increasing_history(tmp_path):
    with pytest.raises(ValueError):
        plot_convergence(
            [10.0, 8.0, 9.0],
            str(tmp_path / "invalid.png"),
        )


def test_convergence_plot_rejects_empty_history(tmp_path):
    with pytest.raises(ValueError):
        plot_convergence([], str(tmp_path / "empty.png"))
