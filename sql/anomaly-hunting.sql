-- Allowed inbound rows
SELECT
    source_ip,
    source_name,
    destination_ip,
    destination_name,
    matched_by,
    SUM(flow_count) AS total_flows,
    COUNT(*) AS row_count
FROM imported_flows
WHERE status = 'OK'
  AND direction_inferred = 'inbound'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Same source IP seen as both blocked and allowed
SELECT
    source_ip,
    source_name,
    SUM(CASE WHEN status = 'Blocked' THEN flow_count ELSE 0 END) AS blocked_flows,
    SUM(CASE WHEN status = 'OK' THEN flow_count ELSE 0 END) AS ok_flows,
    COUNT(DISTINCT matched_by) AS matched_rule_count,
    GROUP_CONCAT(DISTINCT matched_by) AS matched_rules
FROM imported_flows
WHERE source_ip IS NOT NULL
  AND source_ip <> ''
GROUP BY source_ip, source_name
HAVING blocked_flows > 0
   AND ok_flows > 0
ORDER BY blocked_flows DESC, ok_flows DESC
LIMIT 250;

-- Source IPs with multiple source names
SELECT
    source_ip,
    COUNT(DISTINCT source_name) AS distinct_source_names,
    GROUP_CONCAT(DISTINCT source_name) AS source_names,
    SUM(flow_count) AS total_flows,
    COUNT(*) AS row_count
FROM imported_flows
WHERE source_ip IS NOT NULL
  AND source_ip <> ''
GROUP BY source_ip
HAVING COUNT(DISTINCT source_name) >= 2
ORDER BY total_flows DESC, distinct_source_names DESC, row_count DESC
LIMIT 250;

-- Unknown-direction rows
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
GROUP BY source_name, source_ip, destination_name, destination_ip, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Rows where source or destination IP is missing
SELECT
    source_name,
    source_ip,
    destination_name,
    destination_ip,
    matched_by,
    status,
    SUM(flow_count) AS total_flows,
    COUNT(*) AS row_count
FROM imported_flows
WHERE source_ip IS NULL
   OR source_ip = ''
   OR destination_ip IS NULL
   OR destination_ip = ''
GROUP BY source_name, source_ip, destination_name, destination_ip, matched_by, status
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;