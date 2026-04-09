#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import ipaddress
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional
from zoneinfo import ZoneInfo


TIMESTAMP_FORMAT = "%B %d, %Y %I:%M %p"


@dataclass(frozen=True)
class LocalScope:
    local_networks: list[ipaddress._BaseNetwork]
    local_ips: set[str]


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def parse_int(value: Any) -> Optional[int]:
    raw = clean_text(value).replace(",", "")
    if not raw:
        return None
    try:
        return int(float(raw))
    except ValueError:
        return None


def normalize_ip(value: Any) -> Optional[str]:
    raw = clean_text(value)
    if not raw:
        return None
    try:
        return str(ipaddress.ip_address(raw))
    except ValueError:
        return None


def normalize_header_map(row: dict[str, Any]) -> dict[str, str]:
    return {str(key).strip().lower(): key for key in row.keys()}


def get_field(row: dict[str, Any], header_map: dict[str, str], name: str) -> str:
    real_key = header_map.get(name.strip().lower())
    if real_key is None:
        return ""
    return clean_text(row.get(real_key))


def parse_local_networks(values: Iterable[str]) -> list[ipaddress._BaseNetwork]:
    networks: list[ipaddress._BaseNetwork] = []
    for value in values:
        raw = clean_text(value)
        if not raw:
            continue
        networks.append(ipaddress.ip_network(raw, strict=False))
    return networks


def parse_local_ips(values: Iterable[str]) -> set[str]:
    parsed: set[str] = set()
    for value in values:
        ip = normalize_ip(value)
        if ip:
            parsed.add(ip)
    return parsed


def is_internal_or_local(ip: Optional[str], scope: LocalScope) -> bool:
    if not ip:
        return False

    parsed = ipaddress.ip_address(ip)

    if ip in scope.local_ips:
        return True

    for network in scope.local_networks:
        if parsed in network:
            return True

    rfc1918_networks = (
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
    )

    if any(parsed in network for network in rfc1918_networks):
        return True

    if parsed.is_loopback or parsed.is_link_local:
        return True

    return False


def infer_direction(source_ip: Optional[str], destination_ip: Optional[str], scope: LocalScope) -> str:
    src_local = is_internal_or_local(source_ip, scope)
    dst_local = is_internal_or_local(destination_ip, scope)

    if not source_ip and not destination_ip:
        return "unknown"

    if src_local and not dst_local:
        return "outbound"

    if not src_local and dst_local:
        return "inbound"

    if src_local and dst_local:
        return "internal"

    return "unknown"


def derive_remote_local(
    direction: str,
    source_name: str,
    source_ip: Optional[str],
    destination_name: str,
    destination_ip: Optional[str],
) -> tuple[str, Optional[str], str, Optional[str]]:
    if direction == "inbound":
        return source_name, source_ip, destination_name, destination_ip
    if direction == "outbound":
        return destination_name, destination_ip, source_name, source_ip
    return "", None, "", None


def parse_timestamp_with_source_tz(
    timestamp_text: str,
    source_tz_name: str,
) -> tuple[str, str]:
    naive = datetime.strptime(timestamp_text, TIMESTAMP_FORMAT)
    source_tz = ZoneInfo(source_tz_name)

    source_dt = naive.replace(tzinfo=source_tz)
    utc_dt = source_dt.astimezone(timezone.utc)

    return (
        source_dt.replace(microsecond=0).isoformat(),
        utc_dt.replace(microsecond=0).isoformat(),
    )


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = NORMAL;
        PRAGMA foreign_keys = ON;
        PRAGMA busy_timeout = 10000;

        CREATE TABLE IF NOT EXISTS imported_flows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT NOT NULL,
            timestamp_original TEXT NOT NULL,
            timestamp_source_tz TEXT NOT NULL,
            ts_source_iso TEXT NOT NULL,
            ts_utc_iso TEXT NOT NULL,
            status TEXT NOT NULL,
            source_name TEXT,
            source_ip TEXT,
            destination_name TEXT,
            destination_ip TEXT,
            matched_by TEXT,
            upload_bytes INTEGER,
            download_bytes INTEGER,
            flow_count INTEGER NOT NULL DEFAULT 1,
            direction_inferred TEXT NOT NULL,
            remote_name TEXT,
            remote_ip TEXT,
            local_name TEXT,
            local_ip TEXT,
            raw_json TEXT NOT NULL,
            imported_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_imported_flows_status
            ON imported_flows(status);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_direction
            ON imported_flows(direction_inferred);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_remote_ip
            ON imported_flows(remote_ip);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_local_ip
            ON imported_flows(local_ip);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_matched_by
            ON imported_flows(matched_by);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_ts_utc
            ON imported_flows(ts_utc_iso);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_source_ip
            ON imported_flows(source_ip);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_source_name
            ON imported_flows(source_name);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_destination_ip
            ON imported_flows(destination_ip);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_destination_name
            ON imported_flows(destination_name);

        CREATE INDEX IF NOT EXISTS idx_imported_flows_status_direction_matched
            ON imported_flows(status, direction_inferred, matched_by);

        DROP VIEW IF EXISTS v_blocked_inbound_summary;
        CREATE VIEW v_blocked_inbound_summary AS
        SELECT
            source_ip,
            NULLIF(MAX(CASE WHEN source_name IS NOT NULL AND source_name <> '' THEN lower(source_name) ELSE '' END), '') AS source_name,
            SUM(flow_count) AS total_flows,
            COUNT(*) AS row_count,
            COUNT(DISTINCT destination_ip) AS targeted_local_ip_count,
            GROUP_CONCAT(DISTINCT destination_ip) AS targeted_local_ips,
            COUNT(DISTINCT matched_by) AS matched_rule_count,
            GROUP_CONCAT(DISTINCT matched_by) AS matched_rules,
            MIN(ts_utc_iso) AS first_seen_utc,
            MAX(ts_utc_iso) AS last_seen_utc
        FROM imported_flows
        WHERE status = 'Blocked'
          AND direction_inferred = 'inbound'
          AND source_ip IS NOT NULL
          AND source_ip <> ''
        GROUP BY source_ip;

        DROP VIEW IF EXISTS v_blocked_inbound_rule_summary;
        CREATE VIEW v_blocked_inbound_rule_summary AS
        SELECT
            source_ip,
            NULLIF(MAX(CASE WHEN source_name IS NOT NULL AND source_name <> '' THEN lower(source_name) ELSE '' END), '') AS source_name,
            matched_by,
            SUM(flow_count) AS total_flows,
            COUNT(*) AS row_count,
            COUNT(DISTINCT destination_ip) AS targeted_local_ip_count,
            GROUP_CONCAT(DISTINCT destination_ip) AS targeted_local_ips,
            MIN(ts_utc_iso) AS first_seen_utc,
            MAX(ts_utc_iso) AS last_seen_utc
        FROM imported_flows
        WHERE status = 'Blocked'
          AND direction_inferred = 'inbound'
          AND source_ip IS NOT NULL
          AND source_ip <> ''
        GROUP BY source_ip, matched_by;

        DROP VIEW IF EXISTS v_matched_by_summary;
        CREATE VIEW v_matched_by_summary AS
        SELECT
            matched_by,
            SUM(flow_count) AS total_flows,
            COUNT(*) AS row_count,
            COUNT(DISTINCT source_ip) AS distinct_source_ips,
            COUNT(DISTINCT destination_ip) AS distinct_destination_ips,
            MIN(ts_utc_iso) AS first_seen_utc,
            MAX(ts_utc_iso) AS last_seen_utc
        FROM imported_flows
        WHERE status = 'Blocked'
        GROUP BY matched_by;

        DROP VIEW IF EXISTS v_unknown_direction_summary;
        CREATE VIEW v_unknown_direction_summary AS
        SELECT
            source_name,
            source_ip,
            destination_name,
            destination_ip,
            matched_by,
            SUM(flow_count) AS total_flows,
            COUNT(*) AS row_count
        FROM imported_flows
        WHERE direction_inferred = 'unknown'
        GROUP BY source_name, source_ip, destination_name, destination_ip, matched_by;
        """
    )
    conn.commit()


def import_csv(
    conn: sqlite3.Connection,
    csv_path: Path,
    source_tz_name: str,
    scope: LocalScope,
) -> int:
    inserted = 0
    imported_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            header_map = normalize_header_map(row)

            timestamp_original = get_field(row, header_map, "Timestamp")
            status = get_field(row, header_map, "Status")
            source_name = get_field(row, header_map, "Source")
            source_ip = normalize_ip(get_field(row, header_map, "Source IP"))
            destination_name = get_field(row, header_map, "Destination")
            destination_ip = normalize_ip(get_field(row, header_map, "Destination IP"))
            matched_by = get_field(row, header_map, "Matched By")
            upload_bytes = parse_int(get_field(row, header_map, "Upload"))
            download_bytes = parse_int(get_field(row, header_map, "Download"))
            flow_count = parse_int(get_field(row, header_map, "Flow Count")) or 1

            if not timestamp_original:
                continue

            ts_source_iso, ts_utc_iso = parse_timestamp_with_source_tz(
                timestamp_original,
                source_tz_name=source_tz_name,
            )

            direction_inferred = infer_direction(source_ip, destination_ip, scope)
            remote_name, remote_ip, local_name, local_ip = derive_remote_local(
                direction_inferred,
                source_name=source_name,
                source_ip=source_ip,
                destination_name=destination_name,
                destination_ip=destination_ip,
            )

            conn.execute(
                """
                INSERT INTO imported_flows (
                    source_file,
                    timestamp_original,
                    timestamp_source_tz,
                    ts_source_iso,
                    ts_utc_iso,
                    status,
                    source_name,
                    source_ip,
                    destination_name,
                    destination_ip,
                    matched_by,
                    upload_bytes,
                    download_bytes,
                    flow_count,
                    direction_inferred,
                    remote_name,
                    remote_ip,
                    local_name,
                    local_ip,
                    raw_json,
                    imported_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(csv_path),
                    timestamp_original,
                    source_tz_name,
                    ts_source_iso,
                    ts_utc_iso,
                    status,
                    source_name,
                    source_ip,
                    destination_name,
                    destination_ip,
                    matched_by,
                    upload_bytes,
                    download_bytes,
                    flow_count,
                    direction_inferred,
                    remote_name,
                    remote_ip,
                    local_name,
                    local_ip,
                    json.dumps(row, ensure_ascii=False, sort_keys=True),
                    imported_at,
                ),
            )
            inserted += 1

    conn.commit()
    return inserted


def export_ranked_csv(conn: sqlite3.Connection, output_csv: Path, limit: int) -> None:
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

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import Firewalla MSP CSV exports into SQLite, infer direction, and rank blocked inbound source IPs."
    )
    parser.add_argument(
        "--csv",
        nargs="+",
        required=True,
        help="One or more exported Firewalla MSP CSV files.",
    )
    parser.add_argument(
        "--db",
        required=True,
        help="SQLite database path to create or update.",
    )
    parser.add_argument(
        "--source-tz",
        default="UTC",
        help="Timezone the CSV timestamps were originally displayed in. Example: UTC or Europe/Zurich",
    )
    parser.add_argument(
        "--local-cidr",
        action="append",
        default=[],
        help="Repeatable. Local networks to treat as yours, such as 192.168.1.0/24 or 10.0.0.0/8",
    )
    parser.add_argument(
        "--local-ip",
        action="append",
        default=[],
        help="Repeatable. Specific local or public app IPs that belong to you.",
    )
    parser.add_argument(
        "--summary-csv",
        default="blocked_inbound_ranked.csv",
        help="Output CSV for the ranked blocked inbound summary.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="How many ranked rows to export.",
    )
    args = parser.parse_args()

    scope = LocalScope(
        local_networks=parse_local_networks(args.local_cidr),
        local_ips=parse_local_ips(args.local_ip),
    )

    db_path = Path(args.db).expanduser().resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    ensure_schema(conn)

    total_inserted = 0
    for csv_file in args.csv:
        total_inserted += import_csv(
            conn=conn,
            csv_path=Path(csv_file).expanduser().resolve(),
            source_tz_name=args.source_tz,
            scope=scope,
        )

    export_ranked_csv(conn, Path(args.summary_csv).expanduser().resolve(), args.limit)

    top_rows = conn.execute(
        """
        SELECT
            source_ip,
            source_name,
            total_flows,
            targeted_local_ip_count,
            matched_rules
        FROM v_blocked_inbound_summary
        ORDER BY total_flows DESC, row_count DESC, targeted_local_ip_count DESC
        LIMIT 20
        """
    ).fetchall()

    print(f"Imported rows: {total_inserted}")
    print(f"Database: {db_path}")
    print(f"Ranked summary CSV: {Path(args.summary_csv).expanduser().resolve()}")
    print("")
    print("Top 20 blocked inbound source IPs")
    print("source_ip,source_name,total_flows,targeted_local_ip_count,matched_rules")
    for row in top_rows:
        print(",".join("" if value is None else str(value) for value in row))

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())