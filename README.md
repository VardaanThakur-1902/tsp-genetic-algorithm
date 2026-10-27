# Travelling Salesperson Problem Solver Using Genetic Algorithm

A Python-based optimization project that solves the **Travelling Salesperson Problem (TSP)** using a Genetic Algorithm (GA). The system accepts custom cities, their coordinates, and travel costs, then independently searches for the shortest-distance route and the minimum-cost route.

## Overview

The Travelling Salesperson Problem involves finding a tour that visits every city exactly once and returns to the starting city. Finding the globally optimal tour becomes computationally expensive as the number of cities increases.

This project uses a Genetic Algorithm, a population-based optimization technique inspired by natural selection and evolution, to search for good solutions.

The system supports two independent optimization objectives:

- **Shortest-distance optimization:** Minimizes the total geometric distance between cities.
- **Minimum-cost optimization:** Minimizes the total travel cost provided by the user.

Both solutions are evaluated using distance and cost, allowing users to compare the trade-offs between the routes.

## Features

- Accepts a custom number of cities.
- Collects city names and X/Y coordinates interactively.
- Accepts travel costs between city pairs.
- Calculates Euclidean distances automatically.
- Uses a Genetic Algorithm to optimize distance and travel cost separately.
- Implements population initialization, tournament selection, ordered crossover, swap mutation, and elitism.
- Displays the best route, total distance, total cost, and execution time.
- Generates route visualizations using Matplotlib.
- Plots convergence histories for both optimization objectives.
- Generates a distance-versus-cost comparison chart.
- Saves optimization results in JSON format.
- Includes a CSV-based command-line workflow.
- Provides a Random Search baseline, an exact solver for small instances, and evaluation/experiment utilities.
- Includes automated tests using pytest.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core implementation |
| Genetic Algorithm | Route optimization |
| Matplotlib | Route and convergence visualization |
| pytest | Automated testing |
| JSON | Saving optimization results |
| CSV | City input and experimental data |
| Git and GitHub | Version control and project hosting |

## Project Structure

```text
tsp-genetic-algorithm/
│
├── src/
│   ├── __init__.py
│   ├── interactive_solver.py
│   ├── interactive_input.py
│   ├── distance.py
│   ├── genetic_algorithm.py
│   └── visualization.py
│
├── tests/
│   ├── test_distance.py
│   ├── test_genetic_algorithm.py
│   ├── test_interactive_input.py
│   ├── test_dual_optimization.py
│   └── test_dual_visualization.py
│
├── results/
│   ├── dual_optimization_results.json
│   ├── shortest_distance_route.png
│   ├── minimum_cost_route.png
│   ├── dual_convergence.png
│   └── solution_comparison.png
│
├── .gitignore
├── README.md
└── requirements.txt
```

*Note: The files and generated results listed above reflect the intended project structure. Keep only files that actually exist in your repository; generated result files may appear after running the program.*

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Git (optional, for version control)

### 1. Clone the repository

```bash
git clone https://github.com/VardaanThakur-1902/tsp-genetic-algorithm.git
cd tsp-genetic-algorithm
```


### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the virtual environment's Python executable directly instead.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

The `requirements.txt` file should include:

```text
matplotlib
pytest
```

### 4. Verify the installation

```powershell
python --version
python -m pytest -v
```

## Running the Interactive Solver

Start the interactive dual-optimization system from the project root:

```powershell
python -m src.interactive_solver
```

### Step 1: Enter the number of cities

For example:

```text
Enter the number of cities: 4
```

### Step 2: Enter city names and coordinates

Example input:

```text
Name of city 1: Delhi
X coordinate of Delhi: 0
Y coordinate of Delhi: 0

Name of city 2: Jaipur
X coordinate of Jaipur: 3
Y coordinate of Jaipur: 4

Name of city 3: Agra
X coordinate of Agra: 5
Y coordinate of Agra: 1

Name of city 4: Mumbai
X coordinate of Mumbai: 8
Y coordinate of Mumbai: 4
```

Coordinates are numeric values used to calculate geometric distances. They do not have to represent real geographic latitude and longitude.

### Step 3: Enter travel costs

The program asks for the cost between each distinct pair of cities.

```text
Cost from Delhi to Jaipur: 250
Cost from Delhi to Agra: 400
Cost from Delhi to Mumbai: 1200
Cost from Jaipur to Agra: 200
Cost from Jaipur to Mumbai: 900
Cost from Agra to Mumbai: 700
```

The current interactive implementation assumes travel costs are **bidirectional**. The cost from city A to city B is the same as from city B to city A.

### Step 4: View the results

The system runs the Genetic Algorithm twice:

1. Once using the distance matrix as its objective.
2. Once using the travel-cost matrix as its objective.

Each run reports its selected route, total distance, total travel cost, and runtime.

The exact route and numerical results depend on the input and Genetic Algorithm configuration.

## How the Genetic Algorithm Works

### 1. Chromosome representation

Each chromosome represents a complete tour as a permutation of city indices.

For example:

```text
[0, 2, 1, 3]
```

This represents visiting city indices in that order and then returning to city `0`.

The implementation fixes city index `0` as the starting city to avoid generating equivalent tours that differ only by their starting position.

### 2. Population initialization

The algorithm creates an initial population of candidate routes by shuffling the city order while preserving the starting city.

### 3. Fitness evaluation

For a route \(R\), the objective value is:

\[
F(R)=\sum_{i=0}^{n-1}M[R_i][R_{(i+1)\bmod n}]
\]

Here, \(M\) represents either the distance matrix or the travel-cost matrix.

The algorithm minimizes this value. The same route-evaluation logic can therefore optimize both objectives.

### 4. Tournament selection

Tournament selection samples candidate chromosomes and chooses the one with the lowest objective value as a parent.

### 5. Ordered crossover

Ordered crossover combines portions of two parent routes while preserving a valid permutation of the cities.

### 6. Swap mutation

Swap mutation exchanges two city positions, introducing variation into the population.

### 7. Elitism

Elitism carries the best chromosomes into the next generation to preserve strong solutions.

### 8. Convergence tracking

After each generation, the algorithm records the best objective value found so far. These values are used to plot convergence histories.

## Distance Calculation

The project uses Euclidean distance between two coordinates:

\[
d(A,B)=\sqrt{(x_B-x_A)^2+(y_B-y_A)^2}
\]

For example, the distance between coordinates \((0,0)\) and \((3,4)\) is:

\[
d=\sqrt{3^2+4^2}=5
\]

The calculated distance is a geometric distance in the units represented by your coordinates. It is not automatically a road distance or real-world travel time.

## Optimization Objectives

### Shortest-distance route

The Genetic Algorithm minimizes:

\[
D(R)=\sum_{i=0}^{n-1}d(R_i,R_{(i+1)\bmod n})
\]

The corresponding route is evaluated using the supplied cost matrix as well, so its travel cost can be compared.

### Minimum-cost route

The Genetic Algorithm minimizes:

\[
C(R)=\sum_{i=0}^{n-1}c(R_i,R_{(i+1)\bmod n})
\]

The corresponding route is also evaluated using the distance matrix.

The two objectives are optimized independently; the project does not currently combine distance and cost into one weighted objective.

## Generated Results

After a successful interactive run, the visualization functions save the following files under `results/`.

| File | Description |
|---|---|
| `shortest_distance_route.png` | City layout and shortest-distance tour |
| `minimum_cost_route.png` | City layout and minimum-cost tour |
| `dual_convergence.png` | Distance and cost convergence histories |
| `solution_comparison.png` | Comparison of both routes by distance and cost |
| `dual_optimization_results.json` | Input cities, cost matrix, configuration, routes, metrics, and histories |

The exact files generated depend on which commands you run.

The JSON report can be inspected with:

```powershell
Get-Content results\dual_optimization_results.json
```

To list generated plots:

```powershell
Get-ChildItem results\*.png
```

## CSV-Based Workflow

The project also contains a CSV-based command-line entry point. To use it with the default city dataset:

```powershell
python -m src.main
```

To view available command-line options:

```powershell
python -m src.main --help
```

The default city CSV uses the following columns:

```csv
city,x,y
A,0,0
B,2,4
C,5,2
D,6,6
```

The CSV workflow uses the command-line solver's supported options. The interactive solver is the entry point for collecting both custom coordinates and pairwise travel costs.

## Running Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

Run tests for a specific module:

```powershell
python -m pytest tests/test_distance.py -v
```

For the dual-optimization input and matrix logic:

```powershell
python -m pytest tests/test_interactive_input.py -v
python -m pytest tests/test_dual_optimization.py -v
```

For the visualization functions:

```powershell
python -m pytest tests/test_visualization.py -v
python -m pytest tests/test_dual_visualization.py -v
```

The tests cover distance calculations, route validation, Genetic Algorithm operators, input validation, result exporting, evaluation utilities, and visualization file creation.

## Baseline and Exact Solvers

The project also contains two useful reference approaches:

- **Random Search baseline:** samples candidate routes and retains the best one found within a specified number of trials.
- **Exact solver:** enumerates possible tours to find an optimal solution for small instances.

The exact solver has factorial time complexity, approximately \(O((n-1)!)\) tours when the starting city is fixed. It is therefore appropriate only for small datasets.

These solvers can help evaluate the Genetic Algorithm, but their presence does not imply that every run of the project automatically compares all three algorithms.

## Limitations

- The Genetic Algorithm does not guarantee a globally optimal route.
- Solution quality depends on the population size, number of generations, mutation rate, crossover rate, and random seed.
- The interactive implementation assumes symmetric, non-negative travel costs.
- Euclidean distances are based on coordinates, not road networks.
- The current interactive input collects costs manually for every distinct city pair.
- Exact enumeration becomes impractical as the number of cities increases.
- Distance and cost use different units and should not be compared numerically as though they were the same quantity.

## Future Improvements

Potential extensions include:

- Experimental evaluation across multiple random seeds.
- Systematic comparison with Random Search and exact solutions.
- Genetic Algorithm parameter tuning.
- Support for asymmetric travel costs.
- CSV import for travel-cost matrices.
- A graphical user interface or interactive web dashboard.
- Improved route optimization for larger instances.

## Learning Outcomes

This project demonstrates practical implementation of:

- Combinatorial optimization.
- Genetic Algorithms and evolutionary operators.
- Permutation-based chromosome representation.
- Fitness-function design for multiple objectives.
- Distance matrices and cost matrices.
- Python modular programming and unit testing.
- Algorithm visualization and convergence analysis.
- Reproducible experiments and structured result exporting.


**Project:** Travelling Salesperson Problem Solver Using Genetic Algorithm

**Language:** Python

**Core algorithm:** Genetic Algorithm

**Optimization goals:** Shortest distance and minimum travel cost
