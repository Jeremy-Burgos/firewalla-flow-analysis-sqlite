#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path


def export_csv(conn: sqlite3.Connection, output_path: Path, limit: int) -> None:
    rows = conn.execute(
        """
        SELECT
            source_ip,
            source_name,
            total_flows,
            row_count,
            targeted_local_ip_count,
            targeted_local_ips,
            matched_rules,
            first_seen_utc,
            last_seen_utc
        FROM v_blocked_inbound_summary
        ORDER BY total_flows DESC, row_count DESC, targeted_local_ip_count DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "source_ip",
                "source_name",
                "total_flows",
                "row_count",
                "targeted_local_ip_count",
                "targeted_local_ips",
                "matched_rules",
                "first_seen_utc",
                "last_seen_utc",
            ]
        )
        for row in rows:
            writer.writerow(row)


def export_markdown(conn: sqlite3.Connection, output_path: Path, limit: int) -> None:
    rows = conn.execute(
        """
        SELECT
            source_ip,
            source_name,
            total_flows,
            row_count,
            targeted_local_ip_count,
            targeted_local_ips,
            matched_rules,
            first_seen_utc,
            last_seen_utc
        FROM v_blocked_inbound_summary
        ORDER BY total_flows DESC, row_count DESC, targeted_local_ip_count DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    lines: list[str] = []
    lines.append("# Top Blocked Inbound Sources")
    lines.append("")
    lines.append("| Source IP | Source Name | Total Flows | Row Count | Targeted Local IP Count | First Seen UTC | Last Seen UTC |")
    lines.append("|---|---|---:|---:|---:|---|---|")

    for row in rows:
        lines.append(
            f"| {row[0] or ''} | {row[1] or ''} | {row[2] or 0} | {row[3] or 0} | {row[4] or 0} | {row[7] or ''} | {row[8] or ''} |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- This report ranks blocked inbound sources by total flow count.")
    lines.append("- Review `matched_rules` and the underlying raw rows before taking action.")
    lines.append("- High volume alone is not definitive attribution.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export the top blocked inbound source IPs from the SQLite database."
    )
    parser.add_argument("--db", required=True, help="Path to the SQLite database.")
    parser.add_argument("--output", required=True, help="Path to the output file.")
    parser.add_argument(
        "--format",
        choices=["csv", "md"],
        default="csv",
        help="Output format. csv writes a spreadsheet-friendly file. md writes a Markdown summary.",
    )
    parser.add_argument("--limit", type=int, default=100, help="Number of rows to export.")
    args = parser.parse_args()

    db_path = Path(args.db).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    conn = sqlite3.connect(db_path)

    try:
        if args.format == "csv":
            export_csv(conn, output_path, args.limit)
        else:
            export_markdown(conn, output_path, args.limit)
    finally:
        conn.close()

    print(f"Wrote {args.format} output to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())