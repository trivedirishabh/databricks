-- Databricks notebook source
-- Add your gold aggregation query here.
-- Gold: aggregate bike performance for the graph walkthrough.
CREATE OR REFRESH MATERIALIZED VIEW gold_bike_events_mu0dehn6_s3
(
  ride_date DATE COMMENT "Ride date for the aggregation.",
  bike_id STRING COMMENT "Bike identifier.",
  total_rides BIGINT COMMENT "Distinct rides completed by the bike that day.",
  total_revenue DECIMAL(19,4) COMMENT "Daily revenue from the bike.",
  first_start_station_id STRING COMMENT "First station for the day.",
  last_end_station_id STRING COMMENT "Last station for the day."
)
COMMENT "Daily bike-level aggregates for the build-data-pipeline demo."
AS
SELECT
  ride_date,
  bike_id,
  COUNT(DISTINCT ride_id) AS total_rides,
  CAST(SUM(ride_revenue) AS DECIMAL(19,4)) AS total_revenue,
  MIN_BY(start_station_id, start_time) AS first_start_station_id,
  MAX_BY(end_station_id, end_time) AS last_end_station_id
FROM silver_bike_events_mu0dehn6_s3
GROUP BY ALL;
