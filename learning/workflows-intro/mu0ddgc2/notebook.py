# Databricks notebook source
%sql
CREATE SCHEMA IF NOT EXISTS workspace.learning

# COMMAND ----------

%sql
CREATE OR REPLACE VIEW workspace.learning.people AS
SELECT * FROM parquet.`/databricks-datasets/learning-spark-v2/people/people-10m.parquet/`
