# Elastic + Cisco ISE Enrichment and Visualization Checklist

## ISE Auth Flow Visibility in Elastic Maps
- [ ] Set up a working ISE logs ingest pipeline into `cisco_ise-*`
- [ ] Ensure `@timestamp`, `cisco_ise.framed.ip`, `event.outcome`, `cisco_ise.authz_policy`, and geo enrichment fields are present
- [ ] Enrich `client.geo.location` using a `range` enrich policy based on `framed.ip`
- [ ] Enrich `destination.geo.location` using a second enrich policy based on `destination.ip`
- [ ] Add fields like `client.geo.region_name`, `client.geo.name`, etc. for easier filtering
- [ ] Create a map that draws lines from `client.geo.location` to `destination.geo.location`
- [ ] Style lines by `count`, `event.outcome`, or region
- [ ] Save this map and embed it in a Kibana dashboard

## Geo Regions and Choropleths
- [ ] Prepare a GeoJSON file with CONUS, EUROPE, and PAC polygons
- [ ] Import the GeoJSON as a region index (`geo_regions-*`)
- [ ] Join this region index with ISE data on `client.geo.region_name`
- [ ] Optionally enrich `client.geo.region_name` in pipeline

## Interactive Dashboard Controls
- [ ] Add dropdown filters for `event.outcome` and `client.geo.region_name`
- [ ] Add time range and KQL bar filters
- [ ] Save as an interactive âISE Dashboardâ

## Latest Endpoint Status Table
- [ ] Create a Lens âTop hitâ table by `cisco_ise.framed.ip`
- [ ] Show most recent `authz_policy`, `event.outcome`, and `@timestamp`
- [ ] Filter on `authz_policy: "Quarantine"` for status tracking
- [ ] Add this table to the dashboard

## Infrastructure Setup
- [ ] Ensure Kibana container can access internal TMS (ArcGIS)
- [ ] Configure `map.tilemap.url` to point to ArcGIS tile server
- [ ] Validate maps render properly in the air-gapped environment
- [ ] Use time slider and saved ranges

## Bonus: Transform Job
- [ ] Create an Elasticsearch Transform for current endpoint state
- [ ] Use as materialized index for dashboards or alerts
