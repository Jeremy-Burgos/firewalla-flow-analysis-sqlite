-- Top persistent blocked inbound source IPs
SELECT
    source_ip,
    source_name,
    total_flows,
    row_count,
    targeted_local_ip_count,
    targeted_local_ips,
    matched_rule_count,
    matched_rules,
    first_seen_utc,
    last_seen_utc
FROM v_blocked_inbound_summary
ORDER BY total_flows DESC, row_count DESC, targeted_local_ip_count DESC
LIMIT 250;

-- Persistent blocked inbound source IPs hitting more than one local target
SELECT
    source_ip,
    source_name,
    SUM(flow_count) AS total_flows,
    COUNT(*) AS row_count,
    COUNT(DISTINCT destination_ip) AS targeted_local_ip_count,
    GROUP_CONCAT(DISTINCT destination_ip) AS targeted_local_ips,
    GROUP_CONCAT(DISTINCT matched_by) AS matched_rules
FROM imported_flows
WHERE status = 'Blocked'
  AND direction_inferred = 'inbound'
  AND source_ip IS NOT NULL
  AND source_ip <> ''
GROUP BY source_ip, source_name
HAVING COUNT(DISTINCT destination_ip) >= 2
ORDER BY total_flows DESC, targeted_local_ip_count DESC, row_count DESC
LIMIT 250;

-- Most targeted local IPs
SELECT
    destination_ip AS local_ip,
    destination_name AS local_name,
    SUM(flow_count) AS total_flows,
    COUNT(*) AS row_count,
    COUNT(DISTINCT source_ip) AS distinct_remote_sources,
    GROUP_CONCAT(DISTINCT matched_by) AS matched_rules
FROM imported_flows
WHERE status = 'Blocked'
  AND direction_inferred = 'inbound'
  AND destination_ip IS NOT NULL
  AND destination_ip <> ''
GROUP BY destination_ip, destination_name
ORDER BY total_flows DESC, distinct_remote_sources DESC, row_count DESC
LIMIT 250;

-- One source IP drilled down by local target
SELECT
    source_ip,
    source_name,
    destination_ip,
    destination_name,
    matched_by,
    SUM(flow_count) AS total_flows,
    COUNT(*) AS row_count
FROM imported_flows
WHERE status = 'Blocked'
  AND direction_inferred = 'inbound'
  AND source_ip = '203.0.113.10'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC;