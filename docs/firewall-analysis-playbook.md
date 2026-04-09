# Firewall Analysis Playbook

## Start with the blocked inbound sources

The first review pass should answer one practical question:

Which source IPs are repeatedly hitting the network and getting blocked?

Run the persistent inbound query first and sort by:

1. total flows
2. distinct targeted local IPs
3. distinct days

That gives you the cleanest first list of repeat external sources.

## Then review what is being targeted

Once you know which sources are noisy, review the destination side.

You want to know:

- which local IPs are being targeted most
- whether the same internal system appears repeatedly
- whether the same source touches more than one target

That often tells you more than the source count alone.

## Then review `Matched By`

This is where the telemetry stops being a raw network log and starts becoming operationally useful.

You should separate:

- exposure-related blocks such as `Ingress Firewall` or `Port not open`
- device-specific policy blocks
- broad list or feature-based blocks such as ad or DNS filter hits
- odd cases such as `Rule or Feature Not Found`

Do not mix those together when drawing conclusions.

## Then check for allowed inbound rows

Blocked rows show what was stopped.

Allowed inbound rows show what was not stopped and may need a second look, especially if the same source appears in both blocked and allowed traffic.

## Then check the ambiguous rows

Anything classified as `unknown` should be reviewed before it is ignored.

Usually that points to one of these:

- missing local CIDRs
- missing local public IPs
- export rows that lack enough context
- labels that do not match the underlying IP behavior cleanly

## Practical review order

Use this order every time:

1. top blocked inbound source IPs
2. top targeted local IPs
3. top `Matched By` rules
4. top list-driven blocks
5. allowed inbound rows
6. unknown-direction rows
7. one-source-one-target deep review where needed

## What to write down during review

Keep notes on:

- the top repeated source IPs
- the top repeated local targets
- the rules that generate the most volume
- the difference between scanner-style traffic and policy-driven blocks
- anything that looks inconsistent or out of place

That turns the workflow from a one-off query exercise into an operational process.

## What not to do

Do not treat all blocked traffic as the same class of problem.

A repeated inbound source hitting a closed service is not the same signal as a list-based outbound block. They may both be useful, but they answer different questions.

## Related documentation

- [`README.md`](README.md)
- [`methodology.md`](methodology.md)
- [`sql-query-guide.md`](sql-query-guide.md)
- [`matched-by-patterns.md`](matched-by-patterns.md)
- [`limitations-and-false-positives.md`](limitations-and-false-positives.md)