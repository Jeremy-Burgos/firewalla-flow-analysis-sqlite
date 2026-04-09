# Expected Outputs

This file explains what a clean run against the sanitized example dataset should show.

## Example import command

```bash
python scripts/firewalla_csv_to_sqlite.py \
  --csv examples/sample-firewalla-export.csv \
  --db firewalla_flows.sqlite3 \
  --source-tz UTC \
  --local-cidr 192.168.1.0/24 \
  --local-cidr 10.0.0.0/8 \
  --summary-csv blocked_inbound_ranked.csv
````

## Expected highlights

### Top blocked inbound source

The strongest blocked inbound source in the sample should be:

* `203.0.113.10`
* source name: `scanner-alpha.example`
* total blocked inbound flows: `25`

That total comes from:

* `12` via `Ingress Firewall`
* `7` via `Port not open`
* `6` via `Ingress Firewall`

It should target more than one local IP.

### Second inbound source worth noticing

`198.51.100.88` should appear as another strong blocked inbound source with a combined blocked inbound flow count of `13`.

### Device-level inbound policy example

`198.51.100.200` should appear under the TV-device protection rule with a blocked inbound flow count of `11`.

### Rule volume examples

The sample should contain visible rows for:

* `Ingress Firewall`
* `Port not open`
* `Ad Block`
* `Block OISD on All Devices of Firewalla`
* `Block DShield Block List on All Devices of Firewalla`
* `Block North Korea IPs on All Devices of Firewalla`
* `Crypto List`
* `Newly Registered Domains`
* `Tor Exit Nodes`
* `HaGeZi - Multi Pro++`
* `Firewalla's NSFW AI Blocklist`
* `uBlockOrigin's Huge AI Blocklist`
* `Steven Black`
* `AdGuard DNS Filter`
* `Block List Project`
* `Block Remote Port 23 on All Devices of Firewalla`
* `Rule or Feature Not Found`

### Allowed inbound example

The sample includes one `OK` inbound row for `203.0.113.10` so the anomaly query should show that the same source appears in both blocked and allowed traffic.

### Unknown-direction example

The sample includes one row where both source and destination are external:

* source IP: `198.51.100.201`
* destination IP: `203.0.113.201`

That row should land in the unknown-direction view.

## Purpose of the sample

This dataset is synthetic and intentionally small.

It exists to prove that:

* the parser imports correctly
* the SQLite schema works
* the views build correctly
* the SQL query files return meaningful results