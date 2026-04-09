# Dataset Assumptions

## Supported export shape

The current parser is written around a Firewalla MSP CSV export with these columns:

- `Timestamp`
- `Status`
- `Source`
- `Source IP`
- `Destination`
- `Destination IP`
- `Matched By`
- `Upload`
- `Download`
- `Flow Count`

If your export differs from that shape, update the parser or map the columns first.

## Timestamp handling

The export timestamp is treated as display-layer data.

If you convert timestamps during import, the conversion is only as reliable as the source timezone you declare. If you do not care about cross-timezone review, keeping the original text may be enough.

The workflow does not depend on sophisticated time conversion to remain useful.

## Status assumptions

The parser expects `Status` values such as:

- `Blocked`
- `OK`

The SQL workflow is centered on blocked activity first, with supporting queries for allowed inbound rows and ambiguous rows.

## Source and destination assumptions

The parser assumes that `Source IP` and `Destination IP` are the best available network indicators in the export.

`Source` and `Destination` are retained as labels, but the workflow relies on the IP fields for most serious review.

## Matched By assumptions

`Matched By` is operationally important.

It tells you which rule, feature, list, or policy caused the flow to be handled the way it was. That makes it useful for:

- rule tuning
- separating inbound probing from policy-based list blocks
- understanding why volume is appearing in the export

## Flow Count assumptions

`Flow Count` is treated as the main weight for recurrence and ranking.

A row with a higher flow count should carry more weight than a single row with a count of one.

## Direction inference assumptions

When the CSV does not contain a direction field, the parser infers direction from local CIDRs and local IPs.

This works well when:

- your internal ranges are known
- your public application IPs are also provided when needed

This is weaker when:

- your local scope is incomplete
- your environment spans multiple public-facing IPs not supplied to the parser

In those cases, rows may land in `unknown`.

## Privacy assumptions

Real production exports should stay local.

Do not commit raw exports, internal names, or unsanitized screenshots to the repository.

## Related documentation

- [`README.md`](README.md)
- [`methodology.md`](methodology.md)
- [`db-browser-walkthrough.md`](db-browser-walkthrough.md)
- [`limitations-and-false-positives.md`](limitations-and-false-positives.md)