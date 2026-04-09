BEGIN;

CREATE INDEX IF NOT EXISTS idx_imported_flows_status
    ON imported_flows(status);

CREATE INDEX IF NOT EXISTS idx_imported_flows_direction
    ON imported_flows(direction_inferred);

CREATE INDEX IF NOT EXISTS idx_imported_flows_remote_ip
    ON imported_flows(remote_ip);

CREATE INDEX IF NOT EXISTS idx_imported_flows_remote_name
    ON imported_flows(remote_name);

CREATE INDEX IF NOT EXISTS idx_imported_flows_local_ip
    ON imported_flows(local_ip);

CREATE INDEX IF NOT EXISTS idx_imported_flows_matched_by
    ON imported_flows(matched_by);

CREATE INDEX IF NOT EXISTS idx_imported_flows_source_ip
    ON imported_flows(source_ip);

CREATE INDEX IF NOT EXISTS idx_imported_flows_source_name
    ON imported_flows(source_name);

CREATE INDEX IF NOT EXISTS idx_imported_flows_destination_ip
    ON imported_flows(destination_ip);

CREATE INDEX IF NOT EXISTS idx_imported_flows_destination_name
    ON imported_flows(destination_name);

CREATE INDEX IF NOT EXISTS idx_imported_flows_ts_utc
    ON imported_flows(ts_utc_iso);

CREATE INDEX IF NOT EXISTS idx_imported_flows_status_direction_matched
    ON imported_flows(status, direction_inferred, matched_by);

COMMIT;