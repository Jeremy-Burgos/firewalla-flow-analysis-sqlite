# SQL Query Guide

This repository keeps the SQL split by purpose instead of dumping everything into one file.

## File map

### `sql/schema.sql`

Creates the `imported_flows` table.

### `sql/indexes.sql`

Adds the indexes needed for practical local review.

### `sql/views.sql`

Creates reusable views for:

- blocked inbound source summary
- blocked inbound source-by-rule summary
- matched rule summary
- unknown-direction summary

### `sql/inbound-analysis.sql`

Use this when you want to answer questions about:

- persistent blocked inbound sources
- repeated targeting of local systems
- same source hitting multiple targets

### `sql/rule-analysis.sql`

Use this when you want to answer questions about:

- top `Matched By` values
- which rules generate the most blocked activity
- which rules are associated with which remote sources

### `sql/country-and-list-filters.sql`

Use this when you want to filter by:

- country-name rules such as `North Korea`
- list and feature labels such as `Ad Block`, `DShield`, `OISD`, `Tor`, `Newly Registered Domains`, and similar items present in `Matched By`

### `sql/anomaly-hunting.sql`

Use this for:

- allowed inbound rows
- same source IP seen as both blocked and allowed
- unknown-direction rows
- source IPs with multiple source names

## Recommended starting queries

Start with these three:

1. top blocked inbound source IPs
2. top matched rules
3. unknown-direction rows

That gives you the fastest picture of what is going on.

## Practical note

The strongest results usually come from combining two ideas:

- ranking by `SUM(flow_count)`
- separating scanner-style traffic from list-driven blocks

That is the difference between useful review and noisy review.

## Related documentation

- [`README.md`](README.md)
- [`firewall-analysis-playbook.md`](firewall-analysis-playbook.md)
- [`db-browser-walkthrough.md`](db-browser-walkthrough.md)
- [`../sql/`](../sql/)