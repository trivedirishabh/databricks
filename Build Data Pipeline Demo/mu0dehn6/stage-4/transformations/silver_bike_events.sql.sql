-- Databricks notebook source
-- Silver: clean types, derive revenue, and drop impossible ride durations.
CREATE OR REFRESH MATERIALIZED VIEW silver_bike_events_mu0dehn6_s4
(
  ride_date DATE COMMENT "Calendar date for the ride.",
  ride_id STRING COMMENT "Unique ride identifier.",
  start_time TIMESTAMP COMMENT "Timestamp when the ride started.",
  end_time TIMESTAMP COMMENT "Timestamp when the ride ended.",
  start_station_id STRING COMMENT "Station where the ride started.",
  end_station_id STRING COMMENT "Station where the ride ended.",
  bike_id STRING COMMENT "Bike identifier.",
  user_type STRING COMMENT "Membership type for the rider.",
  ride_revenue DECIMAL(19,4) COMMENT "Derived ride revenue for analytics."
)
COMMENT "Cleaned rides data for the demo medallion pipeline."
AS
SELECT
  TO_DATE(start_time) AS ride_date,
  ride_id,
  CAST(start_time AS TIMESTAMP) AS start_time,
  CAST(end_time AS TIMESTAMP) AS end_time,
  start_station_id,
  end_station_id,
  bike_id,
  user_type,
  CAST(
    CASE
      WHEN user_type = "member" THEN (DATEDIFF(MINUTE, CAST(start_time AS TIMESTAMP), CAST(end_time AS TIMESTAMP)) / 60.0) * 10.0
      ELSE (DATEDIFF(MINUTE, CAST(start_time AS TIMESTAMP), CAST(end_time AS TIMESTAMP)) / 60.0) * 15.0
    END AS DECIMAL(19,4)
  ) AS ride_revenue
FROM bronze_bike_events_mu0dehn6_s4
WHERE DATEDIFF(MINUTE, CAST(start_time AS TIMESTAMP), CAST(end_time AS TIMESTAMP)) > 0;
