# DB Browser for SQLite Walkthrough

## Open the database

After importing the CSV, open the SQLite database in DB Browser for SQLite.

Use:

- `File`
- `Open Database`
- select your `.sqlite3` file

## Review the raw table first

Open the `Browse Data` tab and inspect `imported_flows`.

This gives you a quick sanity check that:

- the import worked
- the expected columns exist
- source and destination values look reasonable
- `Matched By` values are populated
- direction inference did not collapse everything into `unknown`

## Then move to the query workflow

Open the `Execute SQL` tab.

Start with the blocked inbound summary query. That should give you the highest-value first pass.

Then run:

- targeted local IP review
- matched rule summary
- unknown-direction review
- list-specific searches

## Sort results deliberately

When the query returns rows, sort by:

- total flows
- distinct days
- distinct targeted local IPs
- last seen timestamp, if present

Those are the fields that usually matter most for recurring blocked activity.

## Save result sets when useful

For larger reviews, save the query output to CSV.

This is useful when you want to:

- compare one export against another
- keep notes outside the database
- review a short list of recurring sources separately

## Keep the workflow disciplined

Do not jump straight to raw rows for every review.

Use this order:

1. summary view
2. grouped rule view
3. anomaly view
4. raw row drill-down for a specific source or target

That keeps the workflow readable and repeatable.

## Related documentation

- [`README.md`](README.md)
- [`sql-query-guide.md`](sql-query-guide.md)
- [`firewall-analysis-playbook.md`](firewall-analysis-playbook.md)
- [`../examples/`](../examples/)