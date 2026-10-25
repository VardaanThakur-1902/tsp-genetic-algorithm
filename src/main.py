
from src.genetic_algorithm import (
    ordered_crossover,
    validate_chromosome,
)


def main():
    parent1 = [0, 1, 2, 3, 4]
    parent2 = [0, 3, 4, 1, 2]

    names = ["A", "B", "C", "D", "E"]

    child1, child2 = ordered_crossover(
        parent1,
        parent2,
        seed=42,
    )

    def display_route(route):
        names_in_route = [names[city] for city in route]
        names_in_route.append(names_in_route[0])
        return " -> ".join(names_in_route)

    print("=" * 45)
    print("PHASE 5: ORDERED CROSSOVER")
    print("=" * 45)

    print("\nParent 1:", display_route(parent1))
    print("Parent 2:", display_route(parent2))

    print("\nChild 1:", display_route(child1))
    print("Child 1 valid:", validate_chromosome(child1, 5))

    print("\nChild 2:", display_route(child2))
    print("Child 2 valid:", validate_chromosome(child2, 5))


if __name__ == "__main__":
    main()
