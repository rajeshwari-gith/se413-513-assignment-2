# Assignment 2 — Coverage, Data-Flow Testing, and Test Doubles

Tests for `summarize_batch_registrations` and `enroll_student` in
`src/registration.py` (starter code, not modified).

## Setup

```
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install pytest pytest-cov
```

## Run the tests

All tests:

```
pytest
```

Only some tests:

```
pytest -m positive
pytest -m negative
```

## Coverage

Statement and branch coverage:

```
pytest --cov --cov-branch --cov-report=term-missing
```

Statement coverage:

```
pytest --cov --cov-report=term-missing
```

## Results

All 7 tests pass. See `test_results.txt`.

Coverage reports are in `coverage_statement.txt` and `coverage_branch.txt`.
The coverage, data-flow, and test double analysis is in `ANALYSIS.md`.
