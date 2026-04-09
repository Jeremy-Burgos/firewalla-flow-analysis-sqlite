-- Top blocked inbound source IPs
SELECT
    source_ip,
    source_name,
    total_flows,
    row_count,
    targeted_local_ip_count,
    targeted_local_ips,
    matched_rules
FROM v_blocked_inbound_summary
ORDER BY total_flows DESC, row_count DESC, targeted_local_ip_count DESC
LIMIT 25;

-- Top matched rules across blocked rows
SELECT
    matched_by,
    total_flows,
    row_count,
    distinct_source_ips
FROM v_matched_by_summary
ORDER BY total_flows DESC, distinct_source_ips DESC, row_count DESC
LIMIT 25;

-- Rows matching Ad Block
SELECT
    source_ip,
    source_name,
    destination_ip,
    destination_name,
    matched_by,
    SUM(flow_count) AS total_flows
FROM imported_flows
WHERE status = 'Blocked'
  AND lower(matched_by) LIKE '%ad block%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC
LIMIT 25;

-- Rows matching DShield
SELECT
    source_ip,
    source_name,
    destination_ip,
    destination_name,
    matched_by,
    SUM(flow_count) AS total_flows
FROM imported_flows
WHERE status = 'Blocked'
  AND lower(matched_by) LIKE '%dshield%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC
LIMIT 25;

-- Same source seen as both blocked and allowed
SELECT
    source_ip,
    source_name,
    SUM(CASE WHEN status = 'Blocked' THEN flow_count ELSE 0 END) AS blocked_flows,
    SUM(CASE WHEN status = 'OK' THEN flow_count ELSE 0 END) AS ok_flows,
    GROUP_CONCAT(DISTINCT matched_by) AS matched_rules
FROM imported_flows
WHERE source_ip IS NOT NULL
  AND source_ip <> ''
GROUP BY source_ip, source_name
HAVING blocked_flows > 0
   AND ok_flows > 0
ORDER BY blocked_flows DESC, ok_flows DESC
LIMIT 25;

-- Unknown-direction rows
SELECT
    source_name,
    source_ip,
    destination_name,
    destination_ip,
    matched_by,
    total_flows,
    row_count
FROM v_unknown_direction_summary
ORDER BY total_flows DESC, row_count DESC
LIMIT 25;