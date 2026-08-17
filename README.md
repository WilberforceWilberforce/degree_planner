# Degree Planner

A scheduling tool that generates balanced 4-year degree plans using graph algorithms and machine learning.

## Overview

Degree Planner uses a greedy scheduling algorithm to balance course load across semesters, models course prerequisites as a directed acyclic graph (DAG), and leverages regression models trained on historical workload data to predict course difficulty.

## Features

- **Greedy Scheduling Algorithm**: Balances course load evenly across semesters
- **DAG-based Prerequisites**: Models course prerequisites and generates valid topological orderings
- **Workload Prediction**: Regression model trained on historical data to estimate course difficulty
- **CLI Interface**: Parses CSV input and outputs personalized 4-year schedules

## Tech Stack

- Java
- Python
- Graph Algorithms
- Machine Learning

## Project Structure

```
degree-planner/
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   └── sample_courses.csv
├── src/
│   ├── java/
│   │   └── com/degreeplanner/
│   └── python/
│       └── scheduler/
└── tests/
```

## Getting Started

### Prerequisites
- Java 11+
- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/WilberforceWilberforce/degree-planner.git
cd degree-planner
```

### Usage

```bash
python -m scheduler --input data/sample_courses.csv --output schedule.txt
```

## License

MIT License - See LICENSE file for details

## Author

[Your Name]
