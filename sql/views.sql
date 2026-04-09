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