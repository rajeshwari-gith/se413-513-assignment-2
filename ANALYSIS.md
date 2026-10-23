# Test Analysis

The two functions tested are `summarize_batch_registrations` (lines 62-89) and
`enroll_student` (lines 92-117) in `src/registration.py`.

## 4. Statement and Branch Coverage

### 4(a) Statement coverage

```
pytest --cov --cov-report=term-missing
```

```
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/registration.py      36      4    89%   25, 28, 31, 50
---------------------------------------------------
TOTAL                    36      4    89%
```

The missing lines (25, 28, 31, 50) are all inside `can_register` and
`calculate_registration_fee`, which are not part of this assignment. No line from
62 onward is missing, so both new functions have 0 missing statements.

Note: `pyproject.toml` sets `branch = true`, so dropping `--cov-branch` still
counts branches. This statement-only output was made with a separate settings
file that turns branch counting off. `src/registration.py` and `pyproject.toml`
were not changed.

### 4(b) Branch coverage

```
pytest --cov --cov-branch --cov-report=term-missing
```

```
Name                  Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------
src/registration.py      36      4     18      4    85%   25, 28, 31, 50
-----------------------------------------------------------------
TOTAL                    36      4     18      4    85%
```

No line or branch arc from 62 onward is missing, so both new functions have
no missing branches.

### Which test covers each decision

| Decision | Outcome | Test |
|---|---|---|
| `for` loop (line 83) | runs the body | `test_batch_with_one_approved_request` runs the loop body for its one request. |
| `for` loop (line 83) | skips the body | `test_empty_batch_returns_zero_count_and_zero_fees` has no requests, so the loop goes straight to the return. |
| `if` in the loop (line 84) | True | `test_batch_with_one_approved_request` has an approved request, so the fee is added. |
| `if` in the loop (line 84) | False | `test_batch_with_only_rejected_request_adds_nothing` has a rejected request, so nothing is added. |
| `if` in `enroll_student` (line 110) | True | `test_enroll_student_allowed_sends_confirmation` is allowed, so a confirmation is sent. |
| `if` in `enroll_student` (line 110) | False | `test_enroll_student_rejected_sends_rejection` is rejected, so a rejection is sent. |

## 5. Data-Flow Testing: `total_fees`

### 5(a) Definitions and uses

| Line | Code | Type |
|---|---|---|
| 81 | `total_fees = 0.0` | Definition d1 (start value) |
| 87 | `total_fees = total_fees + calculate_registration_fee(total_credits)` | Use (c-use, reads the old value) and Definition d2 (writes the new value) |
| 89 | `return approved_count, total_fees` | Use (c-use) |

There are no p-uses, because `total_fees` is never used inside an `if` or loop condition.

### 5(b) DU-pair table

| Pair | Definition | Use | What happens | Test |
|---|---|---|---|---|
| 1 | d1 (line 81) | line 87 | The first approved request adds to the start value 0.0 | `test_batch_with_one_approved_request` |
| 2 | d1 (line 81) | line 89 | Nothing is approved, so 0.0 is returned | `test_empty_batch_returns_zero_count_and_zero_fees`, `test_batch_with_only_rejected_request_adds_nothing` |
| 3 | d2 (line 87) | line 87 | Loop-carried: a later approved request adds to the total from an earlier one | `test_batch_with_two_approved_requests_sums_fees`, `test_batch_with_approved_and_rejected_requests` |
| 4 | d2 (line 87) | line 89 | The total after approvals is returned | `test_batch_with_one_approved_request` |

### 5(c) The loop-carried pair

`test_batch_with_two_approved_requests_sums_fees` uses two approved requests:
(12, 3) costs 1425.0 and (6, 2) costs 800.0, so the total must be 2225.0.

With zero approved requests, line 87 never runs. With one approved request, line
87 runs once and only reads the start value from line 81. The pair needs line 87
to run a second time and read the value it wrote the first time, so at least two
approved requests are needed. All-Defs is already met by one approved request
(each definition reaches some use), but All-Uses needs every definition to
reach every use, including this one.

## 6. Test Doubles

The `notifier` fixture in `tests/conftest.py` returns a plain `Mock`.

| Test | State check | Behavior check |
|---|---|---|
| `test_enroll_student_allowed_sends_confirmation` | returns True | `send_confirmation` called once with 1425.0, `send_rejection` not called |
| `test_enroll_student_rejected_sends_rejection` | returns False | `send_rejection` called once with no arguments, `send_confirmation` not called |
