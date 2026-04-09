# Firewalla Flow Analysis with SQLite

A practical workflow for importing Firewalla flow exports into SQLite and reviewing blocked traffic, repeated inbound activity, rule matches, and defensive patterns with SQL.

## Why this repository exists

Firewall dashboards are useful, but they are not enough when you want to review repeated blocked sources, understand how rules are firing, compare blocked versus allowed activity, or preserve evidence for later analysis.

This repository documents a clear workflow for exporting Firewalla flows, importing them into SQLite, and analyzing them with SQL. The focus is defensive review, repeatable investigation, and clean documentation.

## What this repository does

This repository is designed to help you:

- import Firewalla flow exports into SQLite
- normalize the fields needed for repeatable SQL analysis
- infer direction when the export does not include an explicit direction field
- rank repeated blocked inbound sources
- analyze `Matched By` rule behavior
- review list-based filtering events
- inspect results in DB Browser for SQLite
- build a disciplined review process for firewall data

## What this repository does not do

This repository does not attempt to do the following:

- claim universal malicious attribution for every blocked IP or hostname
- generate a public blocklist automatically
- replace firewall review, validation, or tuning
- treat every blocked event as equally important
- promise perfect direction inference when the export itself is incomplete

## Workflow overview

The workflow is intentionally simple:

1. Export flows from Firewalla MSP.
2. Import the CSV into SQLite with the parsing script.
3. Normalize the data and build SQL views.
4. Review repeated blocked sources, rule matches, and patterns with SQL.
5. Decide what is operationally relevant before taking action.

## Repository structure

- `scripts/` contains the ingestion and helper scripts.
- `sql/` contains schema, indexes, views, and query sets grouped by use case.
- `docs/` contains methodology, assumptions, playbooks, and limitations.
- `examples/` contains sanitized examples for testing and demonstration.
- `screenshots/` contains the screenshot checklist and any sanitized walkthrough images added later.
- `tests/` contains lightweight parser and workflow tests.

## Documentation map

The repository documentation is organized to be read in a practical order.

Start here:

- [`docs/README.md`](docs/README.md)
- [`docs/methodology.md`](docs/methodology.md)
- [`docs/dataset-assumptions.md`](docs/dataset-assumptions.md)
- [`docs/firewall-analysis-playbook.md`](docs/firewall-analysis-playbook.md)
- [`docs/sql-query-guide.md`](docs/sql-query-guide.md)

Supporting references:

- [`docs/db-browser-walkthrough.md`](docs/db-browser-walkthrough.md)
- [`docs/matched-by-patterns.md`](docs/matched-by-patterns.md)
- [`docs/limitations-and-false-positives.md`](docs/limitations-and-false-positives.md)

## Quick start

Create a local environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
````

Import a Firewalla CSV export into SQLite:

```bash
python scripts/firewalla_csv_to_sqlite.py \
  --csv ./examples/sample-firewalla-export.csv \
  --db ./firewalla_flows.sqlite3 \
  --source-tz UTC \
  --local-cidr 192.168.1.0/24 \
  --local-cidr 10.0.0.0/8 \
  --summary-csv ./blocked_inbound_ranked.csv
```

Open the database in DB Browser for SQLite and start with the blocked inbound summary view.

## Core analysis questions

This repository is built around a few practical defensive questions:

* Which source IPs are the most persistent blocked inbound sources?
* Which internal devices or local IPs are being targeted most often?
* Which rules under `Matched By` are firing most often?
* Which list-based blocks are creating the most volume?
* Which events are clear inbound probing versus policy-based filtering?
* Which rows are ambiguous and need manual review?

## Example SQL queries

Top persistent blocked inbound sources:

```sql
SELECT
  source_ip,
  source_name,
  SUM(flow_count) AS total_flows,
  COUNT(*) AS row_count,
  COUNT(DISTINCT destination_ip) AS targeted_local_ip_count,
  GROUP_CONCAT(DISTINCT destination_ip) AS targeted_local_ips,
  GROUP_CONCAT(DISTINCT matched_by) AS matched_rules
FROM imported_flows
WHERE status = 'Blocked'
  AND direction_inferred = 'inbound'
  AND source_ip IS NOT NULL
  AND source_ip <> ''
GROUP BY source_ip, source_name
ORDER BY total_flows DESC, row_count DESC, targeted_local_ip_count DESC
LIMIT 250;
```

Top matched rules:

```sql
SELECT
  matched_by,
  SUM(flow_count) AS total_flows,
  COUNT(*) AS row_count,
  COUNT(DISTINCT source_ip) AS distinct_source_ips
FROM imported_flows
WHERE status = 'Blocked'
GROUP BY matched_by
ORDER BY total_flows DESC, distinct_source_ips DESC, row_count DESC
LIMIT 250;
```

Unknown-direction rows that need closer inspection:

```sql
SELECT
  source_name,
  source_ip,
  destination_name,
  destination_ip,
  matched_by,
  SUM(flow_count) AS total_flows
FROM imported_flows
WHERE direction_inferred = 'unknown'
GROUP BY source_name, source_ip, destination_name, destination_ip, matched_by
ORDER BY total_flows DESC
LIMIT 250;
```

## Defensive use cases

This workflow is useful for:

* reviewing repeated blocked inbound traffic
* identifying repeatedly targeted internal systems
* validating how rules and blocklists are firing
* supporting firewall tuning decisions
* creating local evidence for later investigation
* demonstrating operational logging and SQL-based analysis skills

## Limitations

This repository keeps a strict line between evidence and conclusions.

Important limitations:

* exported timestamps depend on the timezone shown in the source UI
* direction inference depends on accurate local CIDR and local IP assumptions
* rule names are useful operational signals, but they are not definitive threat attribution
* list-based blocking and inbound scanning are not the same signal
* high flow volume does not automatically equal higher severity

## Examples and tests

This repository includes a fully sanitized example dataset and a lightweight test path.

* Example files: [`examples/`](examples/)
* Test files: [`tests/`](tests/)

Use the example dataset first if you want to validate the workflow before running it on your own exports.

## Security notes

Do not commit private exports, secrets, or unsanitized screenshots to this repository.

If you use this workflow on real production data:

* keep raw exports on your own system
* sanitize example data before publishing
* remove internal names, local IPs, and identifying details
* do not publish screenshots containing sensitive device or network information

## Future improvements

Planned future work may include:

* direct MSP API ingestion
* scheduled collection jobs
* optional IP enrichment
* optional country enrichment
* optional dashboards or summary exports

## License

This repository uses the MIT License.

## Final note

This project is intentionally practical, evidence-driven, and built around reproducible review.

The goal is to show disciplined handling of firewall flow exports, defensive review, SQL-based analysis, and operational clarity.