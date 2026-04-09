from __future__ import annotations

import csv
import sqlite3
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "firewalla_csv_to_sqlite.py"
SAMPLE_CSV = REPO_ROOT / "examples" / "sample-firewalla-export.csv"


def run_import(tmp_path: Path) -> tuple[Path, Path]:
    db_path = tmp_path / "firewalla_flows.sqlite3"
    summary_csv = tmp_path / "blocked_inbound_ranked.csv"

    command = [
        sys.executable,
        str(SCRIPT_PATH),
        "--csv",
        str(SAMPLE_CSV),
        "--db",
        str(db_path),
        "--source-tz",
        "UTC",
        "--local-cidr",
        "192.168.1.0/24",
        "--local-cidr",
        "10.0.0.0/8",
        "--summary-csv",
        str(summary_csv),
    ]

    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert db_path.exists()
    assert summary_csv.exists()

    return db_path, summary_csv


def test_example_import_creates_expected_row_count(tmp_path: Path) -> None:
    db_path, _ = run_import(tmp_path)

    conn = sqlite3.connect(db_path)
    count = conn.execute("SELECT COUNT(*) FROM imported_flows").fetchone()[0]
    conn.close()

    assert count == 24


def test_top_blocked_inbound_source_is_scanner_alpha(tmp_path: Path) -> None:
    db_path, _ = run_import(tmp_path)

    conn = sqlite3.connect(db_path)
    row = conn.execute(
        """
        SELECT source_ip, source_name, total_flows, targeted_local_ip_count
        FROM v_blocked_inbound_summary
        ORDER BY total_flows DESC, row_count DESC, targeted_local_ip_count DESC
        LIMIT 1
        """
    ).fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "203.0.113.10"
    assert row[1] == "scanner-alpha.example"
    assert row[2] == 25
    assert row[3] >= 2


def test_ad_block_row_is_classified_as_outbound(tmp_path: Path) -> None:
    db_path, _ = run_import(tmp_path)

    conn = sqlite3.connect(db_path)
    row = conn.execute(
        """
        SELECT direction_inferred, local_ip, remote_ip, flow_count
        FROM imported_flows
        WHERE matched_by = 'Ad Block'
        LIMIT 1
        """
    ).fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "outbound"
    assert row[1] == "192.168.1.15"
    assert row[2] == "93.184.216.34"
    assert row[3] == 15


def test_unknown_direction_view_contains_external_to_external_row(tmp_path: Path) -> None:
    db_path, _ = run_import(tmp_path)

    conn = sqlite3.connect(db_path)
    row = conn.execute(
        """
        SELECT source_ip, destination_ip, total_flows
        FROM v_unknown_direction_summary
        WHERE source_ip = '198.51.100.201'
          AND destination_ip = '203.0.113.201'
        LIMIT 1
        """
    ).fetchone()
    conn.close()

    assert row is not None
    assert row[2] == 1


def test_summary_csv_contains_expected_header_and_top_row(tmp_path: Path) -> None:
    _, summary_csv = run_import(tmp_path)

    with summary_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        first_row = next(reader)

    assert header == [
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
    assert first_row[0] == "203.0.113.10"
    assert first_row[1] == "scanner-alpha.example"
    assert first_row[2] == "25"