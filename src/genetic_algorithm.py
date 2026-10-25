
import math
import random


Chromosome = list[int]


def validate_chromosome(
    chromosome: Chromosome,
    number_of_cities: int,
) -> bool:
    """Return True if a chromosome contains every city exactly once."""
    return (
        number_of_cities >= 1
        and len(chromosome) == number_of_cities
        and chromosome[0] == 0
        and sorted(chromosome) == list(range(number_of_cities))
    )


def create_chromosome(
    number_of_cities: int,
    rng: random.Random,
) -> Chromosome:
    """Create one random route with city 0 fixed at the start."""
    if number_of_cities < 1:
        raise ValueError("At least one city is required.")

    remaining_cities = list(range(1, number_of_cities))
    rng.shuffle(remaining_cities)

    return [0] + remaining_cities


def initialize_population(
    number_of_cities: int,
    population_size: int = 50,
    seed: int | None = 42,
) -> list[Chromosome]:
    """Create a population of random, valid TSP routes."""
    if number_of_cities < 1:
        raise ValueError("At least one city is required.")

    if population_size < 1:
        raise ValueError("Population size must be at least 1.")

    rng = random.Random(seed)
    population = []
    seen = set()

    # Number of distinct tours with city 0 fixed.
    possible_routes = math.factorial(number_of_cities - 1)

    # Try to create unique chromosomes first.
    max_attempts = max(100, population_size * 20)
    attempts = 0

    while (
        len(population) < min(population_size, possible_routes)
        and attempts < max_attempts
    ):
        chromosome = create_chromosome(number_of_cities, rng)
        route_key = tuple(chromosome)

        if route_key not in seen:
            population.append(chromosome)
            seen.add(route_key)

        attempts += 1

    # If uniqueness is exhausted or rare routes were not found,
    # fill the remaining population with valid chromosomes.
    while len(population) < population_size:
        population.append(create_chromosome(number_of_cities, rng))

    return population
