# Methodology

## Purpose

This repository documents a practical workflow for handling firewall flow exports in a way that is structured, repeatable, and useful.

The method is simple:

1. export flows from Firewalla MSP
2. import them into SQLite
3. normalize the fields that matter for review
4. analyze the results with SQL
5. decide what is worth action after review

## Why keeping exports on your own system matters

Firewall flow exports can contain internal device names, internal IP addresses, rule details, and operational context that should not be pushed straight into a public repository.

This workflow keeps the evidence on your own system. It treats the repository as a method, not as a place to store sensitive data.

## Core principles

### Evidence before conclusions

Blocked traffic is evidence of policy enforcement or defensive control. It is not automatic proof of intent, compromise, or universal maliciousness.

### Separate signals by type

This workflow separates at least three different kinds of signals:

- repeated inbound probing
- policy-based list or category blocks
- ambiguous rows that need closer review

Those are not the same thing and should not be treated as the same thing.

### Preserve the original row

The parser stores the original row alongside normalized fields. That gives you an audit trail and lets you re-check assumptions later.

### Review before action

The point of the SQL layer is to support review, not to replace it.

## How direction is inferred

If the export does not include an explicit direction field, the workflow infers direction from local CIDRs and local IPs provided at import time.

The working rule is:

- external source to local destination becomes `inbound`
- local source to external destination becomes `outbound`
- local to local becomes `internal`
- anything that cannot be classified safely becomes `unknown`

That is practical, but it depends on accurate local assumptions.

## Why SQLite

SQLite is enough for this use case.

It is portable, easy to inspect, easy to back up, and easy to open in DB Browser for SQLite. It also makes the workflow simple enough for others to reproduce.

## What this workflow is best at

This workflow is strongest when used to answer questions like:

- which source IPs are the most persistent blocked inbound sources
- which internal systems are targeted most often
- which rules under `Matched By` are firing most often
- which list-based controls produce the most blocked events
- which rows deserve closer review because they do not fit neatly into the expected pattern

## Publication stance

This repository is not a threat-feed project.

It is a workflow project.

That distinction matters. The value here is disciplined parsing, export handling on your own system, SQL analysis, and defensive review.

## Related documentation

- [`README.md`](README.md)
- [`dataset-assumptions.md`](dataset-assumptions.md)
- [`firewall-analysis-playbook.md`](firewall-analysis-playbook.md)
- [`sql-query-guide.md`](sql-query-guide.md)