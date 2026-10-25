
import pytest

from src.genetic_algorithm import (
    create_chromosome,
    initialize_population,
    validate_chromosome,
)
import random


def test_create_chromosome_is_valid():
    rng = random.Random(42)
    chromosome = create_chromosome(5, rng)

    assert validate_chromosome(chromosome, 5)


def test_population_has_requested_size():
    population = initialize_population(
        number_of_cities=5,
        population_size=20,
        seed=42,
    )

    assert len(population) == 20


def test_all_chromosomes_are_valid():
    population = initialize_population(5, 20, seed=42)

    for chromosome in population:
        assert validate_chromosome(chromosome, 5)


def test_population_prefers_unique_routes():
    population = initialize_population(5, 10, seed=42)

    assert len({tuple(route) for route in population}) == 10


def test_same_seed_produces_same_population():
    first = initialize_population(5, 10, seed=42)
    second = initialize_population(5, 10, seed=42)

    assert first == second


def test_single_city_population():
    population = initialize_population(1, 3, seed=42)

    assert population == [[0], [0], [0]]


def test_invalid_city_count():
    with pytest.raises(ValueError):
        initialize_population(0, 10)


def test_invalid_population_size():
    with pytest.raises(ValueError):
        initialize_population(5, 0)


from src.distance import build_distance_matrix
from src.genetic_algorithm import (
    evaluate_fitness,
    tournament_selection,
)


def test_evaluate_fitness_includes_return_trip():
    cities = [(0, 0), (3, 0), (3, 4)]
    matrix = build_distance_matrix(cities)

    distance = evaluate_fitness([0, 1, 2], matrix)

    assert distance == pytest.approx(12.0)


def test_evaluate_fitness_matches_route_distance():
    cities = [(0, 0), (2, 4), (5, 2), (6, 6), (8, 3)]
    matrix = build_distance_matrix(cities)
    route = [0, 2, 4, 1, 3]

    assert evaluate_fitness(route, matrix) == pytest.approx(
        sum(
            matrix[route[i]][route[(i + 1) % len(route)]]
            for i in range(len(route))
        )
    )


def test_invalid_chromosome_rejected_by_fitness():
    matrix = build_distance_matrix([(0, 0), (1, 0), (2, 0)])

    with pytest.raises(ValueError):
        evaluate_fitness([0, 1, 1], matrix)


def test_tournament_returns_a_valid_parent():
    cities = [(0, 0), (2, 4), (5, 2), (6, 6), (8, 3)]
    matrix = build_distance_matrix(cities)
    population = initialize_population(5, 10, seed=42)

    parent = tournament_selection(
        population, matrix, tournament_size=3, seed=123
    )

    assert validate_chromosome(parent, 5)


def test_tournament_selects_best_when_all_contestants_are_sampled():
    cities = [(0, 0), (2, 4), (5, 2), (6, 6), (8, 3)]
    matrix = build_distance_matrix(cities)
    population = initialize_population(5, 10, seed=42)

    parent = tournament_selection(
        population,
        matrix,
        tournament_size=len(population),
        seed=123,
    )

    best_distance = min(
        evaluate_fitness(route, matrix) for route in population
    )

    assert evaluate_fitness(parent, matrix) == pytest.approx(best_distance)


def test_tournament_is_reproducible():
    cities = [(0, 0), (2, 4), (5, 2), (6, 6), (8, 3)]
    matrix = build_distance_matrix(cities)
    population = initialize_population(5, 10, seed=42)

    first = tournament_selection(
        population, matrix, tournament_size=3, seed=123
    )
    second = tournament_selection(
        population, matrix, tournament_size=3, seed=123
    )

    assert first == second


def test_empty_population_rejected():
    matrix = build_distance_matrix([(0, 0), (1, 0)])

    with pytest.raises(ValueError):
        tournament_selection([], matrix)


def test_invalid_tournament_size_rejected():
    matrix = build_distance_matrix([(0, 0), (1, 0)])
    population = initialize_population(2, 3, seed=42)

    with pytest.raises(ValueError):
        tournament_selection(population, matrix, tournament_size=0)
