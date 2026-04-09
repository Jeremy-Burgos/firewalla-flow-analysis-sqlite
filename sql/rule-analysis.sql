-- Top matched rules across all blocked rows
SELECT
    matched_by,
    total_flows,
    row_count,
    distinct_source_ips,
    distinct_destination_ips,
    first_seen_utc,
    last_seen_utc
FROM v_matched_by_summary
ORDER BY total_flows DESC, distinct_source_ips DESC, row_count DESC
LIMIT 250;

-- Blocked inbound sources for Port not open
SELECT
    source_ip,
    source_name,
    SUM(flow_count) AS total_flows,
    COUNT(*) AS row_count,
    GROUP_CONCAT(DISTINCT destination_ip) AS targeted_local_ips
FROM imported_flows
WHERE status = 'Blocked'
  AND direction_inferred = 'inbound'
  AND lower(matched_by) LIKE '%port not open%'
GROUP BY source_ip, source_name
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Blocked inbound sources for Ingress Firewall
SELECT
    source_ip,
    source_name,
    SUM(flow_count) AS total_flows,
    COUNT(*) AS row_count,
    GROUP_CONCAT(DISTINCT destination_ip) AS targeted_local_ips
FROM imported_flows
WHERE status = 'Blocked'
  AND direction_inferred = 'inbound'
  AND lower(matched_by) LIKE '%ingress firewall%'
GROUP BY source_ip, source_name
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Blocked inbound sources for device-level internet blocking
SELECT
    source_ip,
    source_name,
    destination_ip,
    destination_name,
    SUM(flow_count) AS total_flows,
    COUNT(*) AS row_count
FROM imported_flows
WHERE status = 'Blocked'
  AND direction_inferred = 'inbound'
  AND lower(matched_by) LIKE '%block traffic from internet%'
GROUP BY source_ip, source_name, destination_ip, destination_name
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Rows with Rule or Feature Not Found
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
  AND lower(matched_by) LIKE '%rule or feature not found%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Rows for specific remote port block rules
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
  AND lower(matched_by) LIKE '%remote port 23%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;