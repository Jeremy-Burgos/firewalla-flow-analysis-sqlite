# Examples

This folder contains sanitized, public-safe example material.

## Purpose

The example files exist to prove that the workflow is real, reproducible, and easy to test without requiring private firewall exports.

They are meant to support:

- parser validation
- SQL query validation
- DB Browser walkthroughs
- screenshots for the repository
- lightweight tests

## Files

### `sample-firewalla-export.csv`

A Firewalla-style CSV export shaped to match the parser assumptions used in this repository.

It includes examples for:

- blocked inbound scanner-style activity
- device-level inbound blocking
- list-based blocked activity
- one allowed inbound row
- one unknown-direction row

### `sample-queries.sql`

A compact query set that can be run immediately after importing the sample CSV.

### `expected-outputs.md`

Documents what the sample dataset should produce when the workflow is operating correctly.

## Usage

Run the sample import from the repository root:

```bash
python scripts/firewalla_csv_to_sqlite.py \
  --csv examples/sample-firewalla-export.csv \
  --db firewalla_flows.sqlite3 \
  --source-tz UTC \
  --local-cidr 192.168.1.0/24 \
  --local-cidr 10.0.0.0/8 \
  --summary-csv blocked_inbound_ranked.csv
````

Then:

* open the SQLite database in DB Browser for SQLite
* run the example SQL queries
* compare your results to `expected-outputs.md`

## Rules for this folder

Only sanitized or synthetic data belongs here.

Do not add:

* private telemetry
* real internal IP addresses
* real internal hostnames
* real account identifiers
* screenshots with private data visible

## Related files

* [`../README.md`](../README.md)
* [`../docs/README.md`](../docs/README.md)
* [`expected-outputs.md`](expected-outputs.md)
* [`sample-queries.sql`](sample-queries.sql)