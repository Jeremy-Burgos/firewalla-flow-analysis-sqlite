# Tests

This test suite is intentionally light.

The goal is not to build a large testing framework. The goal is to prove that the repository workflow is real, reproducible, and stable enough to trust.

## What the tests cover

The current tests verify that:

- the sanitized example CSV imports successfully
- the SQLite database is created
- the summary CSV is created
- the blocked inbound summary view returns the expected top source
- outbound list-based rows are classified correctly
- unknown-direction rows are preserved instead of being forced into the wrong bucket

## Timestamp model

The workflow keeps:

- the original exported timestamp text
- the declared source timezone
- normalized source-timezone ISO
- normalized UTC ISO

## What the tests do not try to do

These tests do not try to simulate every export variation or every environment.

This repository is a workflow project. The tests are there to confirm that the documented path works and that the example dataset stays aligned with the parser and SQL files.

## Run the tests

```bash
pytest
````

## Design goal

The tests should stay:

* readable
* fast
* easy to run
* easy to trust
* aligned with the documented workflow