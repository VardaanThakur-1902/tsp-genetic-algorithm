
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
