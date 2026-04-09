# Contributing

Thank you for taking the time to review this repository.

This project is focused on a specific use case: importing firewall flow exports into SQLite and analyzing them with SQL. Contributions should improve clarity, reliability, reproducibility, or safety.

## What is welcome

Useful contributions include:

- parser improvements
- SQLite schema or index improvements
- SQL query improvements
- documentation improvements
- reproducibility fixes
- sanitized example data
- workflow validation improvements
- bug fixes that keep the project simple and defensible

## What is not a good fit

This repository is not intended for:

- raw private export uploads
- public threat-feed submissions
- unverifiable malicious-IP claims
- dramatic attribution language
- bloated feature requests that move the project away from its intended scope

## Contribution standards

Please keep contributions aligned with the current direction of the repository:

- security first
- evidence before assumptions
- workflow built around local exports
- clear and reproducible documentation
- minimal unnecessary complexity

## Before opening a pull request

Please make sure that:

- documentation changes are accurate
- SQL examples are tested
- example data is sanitized
- no secrets or private data are included
- the change improves the actual workflow rather than adding noise

## Pull request guidance

A strong pull request should include:

- a clear summary of the change
- the reason the change is needed
- any SQL or parser behavior affected
- any documentation that should be updated alongside the change

## Example data policy

Only sanitized example data belongs in this repository.

Do not include:

- real private exports
- internal hostnames
- internal IP addresses
- personally identifying data
- screenshots containing sensitive details

## Questions and discussion

If you are unsure whether a change fits the scope of the project, open a workflow question first instead of submitting a broad pull request.

Small, precise, defensible improvements are preferred.