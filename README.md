# Degree Planner

A scheduling tool that generates balanced 4-year degree plans using graph algorithms and machine learning.

## Overview

Degree Planner uses a greedy scheduling algorithm to balance course load across semesters, models course prerequisites as a directed acyclic graph (DAG), and leverages regression models trained on historical workload data to predict course difficulty.

## Features

- **Greedy Scheduling Algorithm**: Balances course load evenly across semesters
- **DAG-based Prerequisites**: Models course prerequisites with topological sort for valid orderings
- **Workload Prediction**: Regression model predicts course difficulty based on prerequisites and credit hours
- **CLI Interface**: Parses CSV input and outputs personalized 4-year schedules
- **Cycle Detection**: Validates course prerequisite graph for circular dependencies
- **Comprehensive Testing**: Pytest suite with tests for graph algorithms and scheduling

## Tech Stack

- **Python 3.8+**: Core scheduling engine
- **scikit-learn**: Machine learning for workload prediction
- **pandas/numpy**: Data processing
- **pytest**: Testing framework

## Project Structure

```
degree-planner/
├── README.md
├── LICENSE
├── requirements.txt
├── src/python/
│   ├── __main__.py              # CLI entry point
│   └── scheduler/
│       ├── __init__.py
│       ├── course.py            # Course data model
│       ├── dag.py               # DAG implementation with topological sort
│       ├── workload_predictor.py # ML-based difficulty prediction
│       ├── scheduler.py         # Greedy scheduling algorithm
│       └── csv_parser.py        # CSV parsing utilities
├── data/
│   └── sample_courses.csv       # Sample course dataset
└── tests/
    ├── test_dag.py             # DAG and prerequisite tests
    └── test_scheduler.py       # Scheduling algorithm tests
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

```bash
git clone https://github.com/WilberforceWilberforce/degree_planner.git
cd degree_planner
pip install -r requirements.txt
```

### Usage

Generate a 4-year schedule from a CSV file:

```bash
python -m scheduler --input data/sample_courses.csv --output my_schedule.txt
```

**Options:**
- `--input, -i` (required): Path to CSV file with course data
- `--output, -o`: Output file path (default: `schedule.txt`)
- `--credits, -c`: Target credits per semester (default: `15.0`)
- `--semesters, -s`: Number of semesters (default: `8`)

**Example with custom parameters:**

```bash
python -m scheduler -i data/sample_courses.csv -o schedule.txt -c 16 -s 8
```

### CSV Input Format

Your CSV file should have these columns:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `course_code` | string | Yes | Unique course identifier (e.g., "CS101") |
| `course_name` | string | Yes | Human-readable course name |
| `credits` | integer | Yes | Credit hours for the course |
| `prerequisites` | string | No | Semicolon-separated prerequisite codes (e.g., "CS101;MATH101") |
| `difficulty` | float | No | Difficulty rating 1-5 (default: 1.0) |

**Example:**
```csv
course_code,course_name,credits,prerequisites,difficulty
CS101,Intro to CS,3,,1.0
CS201,Data Structures,4,CS101,2.5
MATH101,Calculus I,4,,2.0
```

### Output Format

The scheduler generates a formatted schedule showing:
- Courses organized by year and semester
- Course code, name, credits, and predicted difficulty
- Total credits per semester
- Total degree credits

## Algorithm Details

### 1. DAG Construction and Validation

The system models courses as nodes in a directed acyclic graph where edges represent prerequisite relationships. The implementation:
- Detects cycles using depth-first search to ensure valid prerequisites
- Raises an error if circular dependencies are found
- Uses Kahn's algorithm for topological sorting

### 2. Greedy Scheduling

The greedy algorithm:
1. For each semester, identifies all available courses (completed prerequisites)
2. Sorts courses by predicted difficulty (easier first) and credit hours
3. Greedily adds courses that fit within the semester credit limit
4. Ensures prerequisites are completed before dependent courses

### 3. Workload Prediction

A linear regression model predicts course difficulty based on:
- Number of prerequisites
- Credit hours
- Historical difficulty data

The model is trained on the input course data and used to inform scheduling decisions.

## Testing

Run the test suite:

```bash
pytest tests/
```

Run with verbose output:

```bash
pytest tests/ -v
```

### Test Coverage

- **DAG Tests**: Topological sorting, cycle detection, prerequisite validation
- **Scheduler Tests**: Valid scheduling, prerequisite respect, credit balancing, schedule generation

## Example

Generate a schedule from sample data:

```bash
python -m scheduler --input data/sample_courses.csv --output output/schedule.txt
```

Output (sample):
```
================================================================================
PERSONALIZED 4-YEAR DEGREE PLAN
================================================================================

YEAR 1 - Fall Semester
--------------------------------------------------------------------------------
  CS101      | Introduction to Computer Science | Credits: 3 | Difficulty: 1.0/5.0
  MATH101    | Calculus I                       | Credits: 4 | Difficulty: 2.0/5.0
  ENG101     | English Composition              | Credits: 3 | Difficulty: 1.5/5.0
  Semester Total: 10 credits

YEAR 1 - Spring Semester
--------------------------------------------------------------------------------
  CS201      | Data Structures                  | Credits: 4 | Difficulty: 2.5/5.0
  MATH201    | Linear Algebra                   | Credits: 4 | Difficulty: 2.5/5.0
  Semester Total: 8 credits

...

================================================================================
TOTAL CREDITS: 36
================================================================================
```

## Performance Characteristics

- **Time Complexity**: O(V + E) for DAG construction and validation
- **Scheduling**: O(C * S) where C is number of courses and S is number of semesters
- **Prediction**: O(C) for ML model inference

## Error Handling

The system gracefully handles:
- Invalid CSV files (missing columns, malformed data)
- Circular prerequisite dependencies
- Courses that cannot be scheduled
- Missing input files

## Future Enhancements

- Multi-objective optimization (minimize difficulty variance, maximize learning progression)
- Constraint satisfaction for course preferences
- Interactive schedule refinement
- Major/concentration requirement tracking
- Co-requisite course handling

## License

MIT License - See LICENSE file for details

## Author

WilberforceWilberforce

## Contact

For questions or contributions, please open an issue on GitHub.
