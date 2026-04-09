# Matched By Patterns

`Matched By` is one of the most useful fields in this workflow because it tells you why the flow was handled the way it was.

It should be read as an operational control signal, not as a final verdict.

## Common patterns

### `Port not open`

This often lines up with scanner-style inbound traffic. It is useful for finding repeated external sources touching closed services.

### `Ingress Firewall`

This is another strong operational signal for blocked inbound attempts against your network edge or controlled exposure points.

### `Block Traffic from Internet on ...`

This usually reflects a device-level protection rule. It is useful for seeing which internet-facing attempts are being stopped by device policy.

### `Ad Block`

This is a policy-based block, not the same thing as an inbound scan. It is still useful, but it should be analyzed separately.

### `Block OISD ...`

This is another list-driven or policy-driven block. Treat it as filtering or policy evidence, not as equivalent to exposure-related inbound attempts.

### `Block DShield Block List ...`

This is useful because it reflects a named defensive list, but it still needs review. A hit on a list is not the same thing as direct proof of hostile intent in your specific environment.

### Country-based rules

Examples such as `Block North Korea ...` are policy signals. They tell you what rule fired. They are not the same thing as a verified geolocation statement.

### `Rule or Feature Not Found`

This deserves review. It may reflect a naming change, export inconsistency, or an operational oddity worth checking again.

### Remote-port block rules

Entries such as `Block Remote Port 23 ...` are direct policy enforcement signals. They are useful for seeing which sources continue to hit disallowed services.

## Practical interpretation

The cleanest way to use `Matched By` is to separate entries into two buckets:

- inbound or exposure-related controls
- list-based or policy-driven controls

That split improves signal quality immediately.

## Related documentation

- [`README.md`](README.md)
- [`firewall-analysis-playbook.md`](firewall-analysis-playbook.md)
- [`limitations-and-false-positives.md`](limitations-and-false-positives.md)
- [`../sql/rule-analysis.sql`](../sql/rule-analysis.sql)