# Travelling Salesperson Problem Solver Using Genetic Algorithm
Artificial Intelligence and Soft Computing (AISC) Project

## 1. Project Overview

A Python-based optimization project that solves the **Travelling Salesperson Problem (TSP)** using a **Genetic Algorithm (GA)**. The system accepts custom cities, their coordinates, and travel costs, then independently searches for the shortest-distance route and the minimum-cost route.
The Travelling Salesperson Problem is a well-known combinatorial optimization problem in which a salesperson must:

- Visit every city exactly once.
- Return to the starting city.
- Minimize the total distance travelled or the total travelling cost.

Finding the optimal solution becomes increasingly difficult as the number of cities increases because the number of possible routes grows factorially.

This project uses a Genetic Algorithm, a population-based optimization technique inspired by the principles of natural selection and biological evolution, to search for efficient solutions.

The project supports two independent optimization modes:

1. **Shortest Distance Optimization:** Finds a route that minimizes the total geographical distance.
2. **Minimum Cost Optimization:** Finds a route that minimizes the total travelling cost.

Both optimization modes are executed separately.

---

## 2. Objectives

The main objectives of this project are:

- To understand and implement the Travelling Salesperson Problem.
- To apply Genetic Algorithms to a real-world optimization problem.
- To implement population initialization and fitness evaluation.
- To implement tournament selection.
- To implement Ordered Crossover (OX).
- To implement Swap Mutation.
- To use elitism to preserve the best solutions.
- To optimize routes based on both distance and cost.
- To visualize the optimization process using Matplotlib.
- To evaluate the effectiveness of the algorithm through testing.

---

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| NumPy | Numerical calculations and array operations |
| Matplotlib | Route and convergence visualization |
| JSON | Storing optimization results |
| Pytest | Automated testing |
| Git and GitHub | Version control and project hosting |

---

## 4. Understanding the Travelling Salesperson Problem

Suppose there are four cities: A, B, C, and D.

The salesperson must visit all four cities exactly once and return to the starting city.

An example route is:

A → B → C → D → A

The objective is to find the best possible arrangement of cities that minimizes the total distance or cost.

### Distance Calculation

When coordinates are provided for each city, Euclidean distance is calculated using:

\[
d(i,j)=\sqrt{(x_j-x_i)^2+(y_j-y_i)^2}
\]

Where:

- \(x_i,y_i\) represent the coordinates of city i.
- \(x_j,y_j\) represent the coordinates of city j.
- \(d(i,j)\) represents the distance between the two cities.

### Total Route Distance

For a route containing n cities:

\[
D=\sum_{i=0}^{n-1}d(c_i,c_{(i+1)\bmod n})
\]

The modulo operation ensures that the final city is connected back to the starting city.

### Cost Optimization

The project also supports a user-provided cost matrix.

The total cost of a route is calculated by adding the travelling costs between consecutive cities, including the return journey.

\[
C=\sum_{i=0}^{n-1}Cost(c_i,c_{(i+1)\bmod n})
\]

Distance and cost are optimized independently.

---

## 5. What Is a Genetic Algorithm?

A Genetic Algorithm is a metaheuristic optimization technique inspired by biological evolution.

It works with a population of possible solutions and repeatedly improves them through selection, crossover, and mutation.

The main stages are:

1. **Population Initialization:** Generate an initial population of possible routes.
2. **Fitness Evaluation:** Calculate the distance or cost of each route.
3. **Selection:** Select better routes as parents.
4. **Crossover:** Combine two parent routes to generate offspring.
5. **Mutation:** Introduce small changes to offspring.
6. **Elitism:** Preserve the best individuals from the current generation.
7. **Replacement:** Form a new population.
8. **Termination:** Repeat the process until the specified number of generations is completed.

### Genetic Algorithm Workflow

```text
          Start
            |
            v
     Enter City Details
            |
            v
    Generate Initial Population
            |
            v
      Evaluate Fitness
            |
            v
      Select Parents
            |
            v
     Ordered Crossover
            |
            v
       Swap Mutation
            |
            v
          Elitism
            |
            v
     Create New Population
            |
            v
    More Generations?
        /       \
      Yes        No
       |          |
       v          v
    Repeat    Best Route
                  |
                  v
                 End
```

---

## 6. Genetic Algorithm Techniques Used

### 6.1 Chromosome Representation

Each possible solution is represented as a chromosome.

In this project, a chromosome represents a route containing all cities.

Example:

```python
[A, C, B, D]
```

This means the salesperson travels from A to C, then B, then D, and finally returns to A.

Each city appears exactly once in a valid chromosome.

### 6.2 Population Initialization

A population consists of multiple randomly generated routes.

For example:

```text
Population:

[A, B, C, D]
[B, D, A, C]
[C, A, D, B]
[D, C, B, A]
```

A larger population provides more initial candidate solutions and increases the diversity of the search.

### 6.3 Fitness Evaluation

Fitness evaluation measures the quality of each candidate route.

For minimization problems, shorter distances or lower costs represent better solutions.

The algorithm compares routes based on their objective values and attempts to improve them over successive generations.

### 6.4 Tournament Selection

Tournament Selection is used to select parents.

Working:

1. Randomly select a small group of individuals.
2. Compare their fitness values.
3. Select the best individual from that group.
4. Repeat the process to select another parent.

This gives better individuals a higher chance of reproduction while maintaining some population diversity.

### 6.5 Ordered Crossover (OX)

Ordered Crossover is a genetic operator designed for permutation-based problems such as TSP.

It combines two parent routes without introducing duplicate cities.

Example:

```text
Parent 1: A B | C D | E F
Parent 2: D F | A E | B C
```

The algorithm:

1. Selects two crossover positions.
2. Copies the selected segment from the first parent.
3. Takes the remaining cities from the second parent in their existing cyclic order.
4. Skips cities already present in the copied segment.
5. Fills the remaining positions.

The resulting child contains every city exactly once.

This is important because ordinary single-point crossover could generate invalid TSP routes containing duplicate or missing cities.

### 6.6 Swap Mutation

Swap Mutation introduces diversity into the population.

Working:

1. Randomly select two positions in a chromosome.
2. Exchange the cities at those positions.
3. Produce a modified route.

Example:

```text
Before Mutation:

[A, B, C, D, E]

After Mutation:

[A, D, C, B, E]
```

Mutation helps the algorithm explore new possible routes and reduces the risk of getting stuck in a local optimum.

### 6.7 Elitism

Elitism ensures that the best individuals from the current generation are preserved in the next generation.

For example, if the elite count is 1, the best route is copied directly into the next population.

This prevents the algorithm from losing its best solution due to crossover or mutation.

---

## 7. Optimization Modes

The project maintains two separate optimization processes.

### Mode 1: Shortest Distance Optimization

The objective is to minimize the total Euclidean distance travelled.

\[
\text{Minimize } D
\]

The distance between cities is calculated using their X and Y coordinates.

### Mode 2: Minimum Cost Optimization

The objective is to minimize the total travelling cost.

\[
\text{Minimize } C
\]

The algorithm uses the user-provided cost matrix to evaluate routes.

### Why Are They Separate?

The shortest route is not necessarily the cheapest route.

For example:

| Route | Total Distance | Total Cost |
|---|---:|---:|
| Route A | 100 km | ₹1,500 |
| Route B | 120 km | ₹1,000 |

Route A is better for distance optimization, whereas Route B is better for cost optimization.

Therefore, the project runs the Genetic Algorithm independently for each objective.

---

## 8. Genetic Algorithm Parameters

The algorithm uses the following parameters:

| Parameter | Default Value | Purpose |
|---|---:|---|
| population_size | 50 | Number of candidate routes in each generation |
| generations | 100 | Number of evolutionary iterations |
| crossover_rate | 0.9 | Probability of performing crossover |
| mutation_rate | 0.1 | Probability of performing mutation |
| tournament_size | 3 | Number of individuals competing in tournament selection |
| elite_count | 1 | Number of best individuals preserved |
| seed | 42 | Random seed for reproducibility |

These are configurable experimental values, not universally optimal values.

Changing these parameters can affect convergence speed, population diversity, and solution quality.

---

## 9. Visualization

The project uses Matplotlib to visualize the optimization results.

The visualizations help understand how the Genetic Algorithm improves its solutions.

The project includes:

1. **Distance Route Visualization:** Displays the optimized route based on geographical coordinates.
2. **Cost Route Visualization:** Displays the route obtained through cost optimization.
3. **Distance Convergence Plot:** Shows how the best distance changes across generations.
4. **Cost Convergence Plot:** Shows how the best cost changes across generations.

### Convergence Graph

A convergence graph plots the best objective value against the number of generations.

The graph helps determine whether the algorithm is improving its solutions over time and whether the population is approaching convergence.

All generated plots are saved in the `results/` directory.

---

## 10. Project Execution Workflow

The interactive workflow allows users to:

1. Enter the number of cities.
2. Enter the name of each city.
3. Enter the X and Y coordinates of every city.
4. Provide the travelling cost matrix.
5. Execute the shortest-distance optimization.
6. Execute the minimum-cost optimization.
7. View the optimized routes and their corresponding values.
8. Generate visualizations.
9. Save the optimization results in JSON format.

The project produces separate results for distance and cost optimization.

---

## 11. Results and Output

The project generates the following outputs:

- Best route for shortest-distance optimization.
- Minimum total geographical distance.
- Best route for minimum-cost optimization.
- Minimum total travelling cost.
- Convergence history for both optimization processes.
- Route visualization plots.
- Convergence visualization plots.
- JSON file containing optimization results.

The results allow users to compare the two optimization objectives independently.

---

## 12. Testing

The project uses Pytest for automated testing.

Testing helps verify that the Genetic Algorithm and its supporting functions work correctly.

Important areas covered include:

- Population generation.
- Route validity.
- Distance calculation.
- Cost calculation.
- Tournament selection.
- Ordered crossover.
- Swap mutation.
- Elitism.
- Genetic Algorithm execution.
- Separate distance and cost optimization.
- Visualization functionality.

Run the test suite using:

```bash
pytest
```

---

## 13. Advantages

- Handles permutation-based optimization problems.
- Supports two independent optimization objectives.
- Uses evolutionary search rather than exhaustive route enumeration.
- Maintains valid city permutations through Ordered Crossover and Swap Mutation.
- Preserves the best solutions using elitism.
- Provides visual representations of optimized routes.
- Allows configurable Genetic Algorithm parameters.
- Supports reproducible experiments using a random seed.

## 14. Limitations

- Genetic Algorithms do not guarantee the globally optimal solution.
- Results depend on parameter settings and initial population diversity.
- Large populations and more generations increase computation time.
- The quality of the solution may vary with different random seeds.
- Euclidean distance assumes straight-line travel rather than actual road distances.
- The cost optimization depends on the accuracy of the supplied cost matrix.

---

## 15. Future Scope

The project can be extended through:

- Hybrid Genetic Algorithms with local search techniques.
- Comparison with Simulated Annealing and Ant Colony Optimization.
- Dynamic city and cost updates.
- Real-world road distance integration.
- Adaptive mutation and crossover rates.
- Larger-scale optimization experiments.
- Multi-objective optimization considering distance and cost simultaneously.

---

## 16. Conclusion

This project demonstrates the application of Genetic Algorithms to solve the Travelling Salesperson Problem.

It implements important evolutionary operators, including Tournament Selection, Ordered Crossover, Swap Mutation, and Elitism.

A key feature is its support for two independent optimization modes: shortest-distance optimization and minimum-cost optimization.

The project also includes Matplotlib visualizations, JSON result storage, and automated testing.

Overall, it demonstrates how concepts from Artificial Intelligence and Soft Computing can be applied to combinatorial optimization problems using evolutionary computation.

---

## 17. Author

Vardaan Thakur Registration Number :- 2427030052 Section-E

**Project:** Travelling Salesperson Problem Solver Using Genetic Algorithm

**Subject:** Artificial Intelligence and Soft Computing (AISC)

**Language:** Python

**Algorithm:** Genetic Algorithm