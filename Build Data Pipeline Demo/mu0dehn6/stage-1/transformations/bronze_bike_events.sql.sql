-- Databricks notebook source
-- Your task: ingest all raw bike events
-- Create a streaming table that reads every field from the source

-- Bronze: load raw bike-share CSV files from a managed volume directory.
CREATE OR REFRESH MATERIALIZED VIEW bronze_bike_events_mu0dehn6_s1
COMMENT "Raw rides loaded from CSV files uploaded by the build-data-pipeline demo."
AS
SELECT *
FROM read_files("/Volumes/dbacademy/default/raw_data/rides/build_data_pipeline_demo", format => "csv", header => true);
