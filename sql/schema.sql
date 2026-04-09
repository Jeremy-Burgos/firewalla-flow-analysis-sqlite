BEGIN;

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

COMMIT;