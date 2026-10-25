
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


from collections.abc import Sequence


def evaluate_fitness(
    chromosome: Chromosome,
    distance_matrix: Sequence[Sequence[float]],
) -> float:
    """Return the total route distance; lower is better."""
    number_of_cities = len(distance_matrix)

    if not validate_chromosome(chromosome, number_of_cities):
        raise ValueError("Invalid chromosome.")

    total_distance = 0.0

    for i in range(len(chromosome)):
        current_city = chromosome[i]
        next_city = chromosome[(i + 1) % len(chromosome)]

        total_distance += distance_matrix[current_city][next_city]

    return total_distance


def tournament_selection(
    population: list[Chromosome],
    distance_matrix: Sequence[Sequence[float]],
    tournament_size: int = 3,
    seed: int | None = None,
) -> Chromosome:
    """Select the shortest-distance chromosome from a random tournament."""
    if not population:
        raise ValueError("Population cannot be empty.")

    if tournament_size < 1 or tournament_size > len(population):
        raise ValueError(
            "Tournament size must be between 1 and population size."
        )

    rng = random.Random(seed)

    contestants = rng.sample(population, tournament_size)

    winner = min(
        contestants,
        key=lambda chromosome: evaluate_fitness(
            chromosome, distance_matrix
        ),
    )

    # Return a copy so later operators cannot modify the population.
    return winner.copy()


def ordered_crossover(
    parent1: Chromosome,
    parent2: Chromosome,
    seed: int | None = None,
    cut_points: tuple[int, int] | None = None,
) -> tuple[Chromosome, Chromosome]:
    """
    Perform Ordered Crossover (OX) on two TSP chromosomes.

    City 0 remains fixed at the start.
    Cut points are inclusive positions within the remaining
    city sequence (excluding city 0).
    """
    n = len(parent1)

    if n != len(parent2):
        raise ValueError("Parents must have the same length.")

    if not validate_chromosome(parent1, n):
        raise ValueError("Parent 1 is invalid.")

    if not validate_chromosome(parent2, n):
        raise ValueError("Parent 2 is invalid.")

    # With fewer than two movable cities, crossover has no effect.
    tail_length = n - 1

    if tail_length < 2:
        return parent1.copy(), parent2.copy()

    rng = random.Random(seed)

    if cut_points is None:
        left, right = sorted(rng.sample(range(tail_length), 2))
    else:
        left, right = cut_points

        if not (0 <= left < right < tail_length):
            raise ValueError(
                "Cut points must satisfy 0 <= left < right < "
                "number of movable cities."
            )

    def make_child(
        segment_parent: Chromosome,
        order_parent: Chromosome,
    ) -> Chromosome:
        segment = segment_parent[1:]
        order = order_parent[1:]

        child = [None] * tail_length

        # Copy the selected segment from the first parent.
        child[left:right + 1] = segment[left:right + 1]

        used = set(child[left:right + 1])

        # Visit positions cyclically, beginning after the right cut.
        positions = [
            (right + 1 + offset) % tail_length
            for offset in range(tail_length)
        ]

        # Read the second parent's sequence in the same cyclic order.
        ordered_cities = [
            order[(right + 1 + offset) % tail_length]
            for offset in range(tail_length)
        ]

        available_cities = [
            city for city in ordered_cities if city not in used
        ]

        for position, city in zip(
            [p for p in positions if child[p] is None],
            available_cities,
        ):
            child[position] = city

        return [0] + child

    child1 = make_child(parent1, parent2)
    child2 = make_child(parent2, parent1)

    return child1, child2


def swap_mutation(
    chromosome: Chromosome,
    mutation_rate: float = 0.1,
    seed: int | None = None,
) -> Chromosome:
    """
    With the given probability, swap two cities in a chromosome.

    City 0 remains fixed. The original chromosome is not modified.
    """
    if not chromosome:
        raise ValueError("Chromosome cannot be empty.")

    if not validate_chromosome(chromosome, len(chromosome)):
        raise ValueError("Invalid chromosome.")

    if not 0.0 <= mutation_rate <= 1.0:
        raise ValueError("Mutation rate must be between 0 and 1.")

    mutated = chromosome.copy()
    rng = random.Random(seed)

    # No mutation is possible with fewer than two movable cities.
    if len(mutated) < 3:
        return mutated

    if rng.random() < mutation_rate:
        pos1, pos2 = rng.sample(range(1, len(mutated)), 2)
        mutated[pos1], mutated[pos2] = (
            mutated[pos2],
            mutated[pos1],
        )

    return mutated


def select_elites(
    population: list[Chromosome],
    distance_matrix: Sequence[Sequence[float]],
    elite_count: int = 1,
) -> list[Chromosome]:
    """
    Return copies of the best chromosomes, ordered by distance.

    These chromosomes can be copied unchanged into the next generation.
    """
    if not population:
        raise ValueError("Population cannot be empty.")

    if not 1 <= elite_count <= len(population):
        raise ValueError(
            "Elite count must be between 1 and population size."
        )

    number_of_cities = len(distance_matrix)

    for chromosome in population:
        if not validate_chromosome(chromosome, number_of_cities):
            raise ValueError("Population contains an invalid chromosome.")

    ranked_population = sorted(
        population,
        key=lambda chromosome: evaluate_fitness(
            chromosome, distance_matrix
        ),
    )

    return [
        chromosome.copy()
        for chromosome in ranked_population[:elite_count]
    ]
