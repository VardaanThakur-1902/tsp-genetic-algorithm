import pytest

from src.interactive_input import collect_problem_input


def test_collects_cities_and_bidirectional_costs(monkeypatch):
    answers = iter([
        "2",
        "Delhi", "0", "0",
        "Jaipur", "3", "4",
        "250",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    cities, labels, costs = collect_problem_input()

    assert cities == [(0.0, 0.0), (3.0, 4.0)]
    assert labels == ["Delhi", "Jaipur"]
    assert costs == [[0.0, 250.0], [250.0, 0.0]]


def test_rejects_fewer_than_two_cities(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    with pytest.raises(ValueError, match="at least 2"):
        collect_problem_input()


def test_rejects_negative_cost(monkeypatch):
    answers = iter([
        "2",
        "Delhi", "0", "0",
        "Jaipur", "3", "4",
        "-100",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    with pytest.raises(ValueError, match="non-negative"):
        collect_problem_input()


def test_rejects_duplicate_city_names(monkeypatch):
    answers = iter([
        "2",
        "Delhi", "0", "0",
        "Delhi",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    with pytest.raises(ValueError, match="Duplicate"):
        collect_problem_input()