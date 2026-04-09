-- Country-name rule filter: North Korea
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
  AND lower(matched_by) LIKE '%north korea%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Crypto List
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
  AND lower(matched_by) LIKE '%crypto list%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Log4j attackers
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
  AND lower(matched_by) LIKE '%log4j attackers%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Newly Registered Domains
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
  AND lower(matched_by) LIKE '%newly registered domains%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- NSFW AI List
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
  AND lower(matched_by) LIKE '%nsfw ai list%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Tor Exit Nodes
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
  AND lower(matched_by) LIKE '%tor exit nodes%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Tor Full Nodes
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
  AND lower(matched_by) LIKE '%tor full nodes%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- AdGuard DNS Filter
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
  AND lower(matched_by) LIKE '%adguard dns filter%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Block List Project
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
  AND lower(matched_by) LIKE '%block list project%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- Ad Block
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
  AND lower(matched_by) LIKE '%ad block%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;

-- DShield
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
  AND lower(matched_by) LIKE '%dshield%'
GROUP BY source_ip, source_name, destination_ip, destination_name, matched_by
ORDER BY total_flows DESC, row_count DESC
LIMIT 250;