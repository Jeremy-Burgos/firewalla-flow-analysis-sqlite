# Security Policy

## Purpose

This repository documents a workflow for importing firewall flow exports into SQLite and analyzing them with SQL.

Because firewall exports can contain sensitive operational data, this repository should be handled carefully even though it is not a live security service.

## Scope

This repository is intended for:

- workflow documentation
- parser logic
- SQL-based analysis
- sanitized examples
- defensive monitoring education

This repository is not intended to host private production exports, secrets, or unsanitized investigation data.

## Supported branch

Security fixes should target:

- `main`

## Reporting a vulnerability

Do not open a public issue for a security problem.

If you discover a vulnerability in the scripts, workflow logic, or repository configuration, report it privately through GitHub private reporting if enabled or through the direct contact method used for other repositories under this profile.

## Security expectations

When using or contributing to this repository:

- never commit raw private firewall exports
- never commit API tokens, credentials, or secrets
- never commit screenshots containing internal names, internal IPs, or identifying details
- sanitize all example data before publication
- keep production export data on your own system unless it has been deliberately redacted

## Operational cautions

This repository analyzes evidence. It does not provide definitive attribution.

Blocked traffic does not automatically equal confirmed malicious activity, and policy-based blocks should not be treated as identical to inbound scanning or attempted service exposure.

Users are expected to review outputs critically before taking action.

## Hardening recommendations

If you adapt this workflow for production use:

- keep exports and databases outside the public repository
- use separate working copies for private and public material
- apply least-privilege access to local storage
- review SQL outputs before sharing findings
- avoid publishing identifiable internal network details

## Disclosure quality

If a future public-facing version of this workflow is ever built around shared findings, it should include:

- methodology
- limitations
- review thresholds
- suppression rules
- removal process