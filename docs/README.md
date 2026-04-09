# Documentation Map

This folder contains the supporting documentation for the firewall flow analysis workflow.

## Start here

If you are new to the repository, read these in order:

1. [`../README.md`](../README.md)
2. [`methodology.md`](methodology.md)
3. [`dataset-assumptions.md`](dataset-assumptions.md)
4. [`firewall-analysis-playbook.md`](firewall-analysis-playbook.md)
5. [`sql-query-guide.md`](sql-query-guide.md)

## File guide

### `methodology.md`

Explains the operating model of the workflow:
what gets imported, how the parser works, how SQL analysis fits in, and why the repository keeps real exports on your own system.

### `dataset-assumptions.md`

Defines the expected CSV shape and the assumptions the parser makes about fields, timestamps, and direction inference.

### `firewall-analysis-playbook.md`

Covers the practical investigation order:
what to look at first, how to separate signal types, and how to review results without collapsing everything into one bucket.

### `sql-query-guide.md`

Maps the SQL files to their use cases and gives the clean starting path for analysis.

### `db-browser-walkthrough.md`

Shows how to use DB Browser for SQLite with this workflow.

### `matched-by-patterns.md`

Explains how to interpret common `Matched By` values without overstating what they mean.

### `limitations-and-false-positives.md`

Explains where the workflow is strong, where it is weak, and why review still matters.

## Practical reading path

If your goal is to run the workflow locally and review blocked inbound activity:

- read [`dataset-assumptions.md`](dataset-assumptions.md)
- run the parser from [`../README.md`](../README.md)
- open the database using [`db-browser-walkthrough.md`](db-browser-walkthrough.md)
- use the SQL files referenced in [`sql-query-guide.md`](sql-query-guide.md)

## Related repository areas

- SQL files live in [`../sql/`](../sql/)
- scripts live in [`../scripts/`](../scripts/)
- sanitized examples live in [`../examples/`](../examples/)
- lightweight tests live in [`../tests/`](../tests/)