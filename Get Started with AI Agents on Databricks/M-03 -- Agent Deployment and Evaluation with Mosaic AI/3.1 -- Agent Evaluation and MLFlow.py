# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Agent Evaluation and MLFlow

# COMMAND ----------

# MAGIC %md
# MAGIC ### Prepare for Production
# MAGIC
# MAGIC Moving from development to deployment requires rigorous testing with high-confidence evaluation. To ensure your agents perform reliably, Databricks provides LLM judges developed by Mosaic AI Research, which offer industry-leading speed and quality measurement for your outputs. 
# MAGIC
# MAGIC You also have access to Agent Evaluation tools that automatically pinpoint the likely root causes of any quality issues, allowing developers to iterate quickly. 
# MAGIC
# MAGIC In addition, Simple UIs streamline the review process, making it easy to compare multiple versions of your Agent side-by-side to ensure only the best models reach your users.

# COMMAND ----------

# MAGIC %md
# MAGIC ### MLFlow Tracing
# MAGIC
# MAGIC ![prepare-for-production.png](../Includes/images/prepare-for-production.png "prepare-for-production.png")
# MAGIC
# MAGIC To move from a prototype to a production-grade application, Databricks provides comprehensive debugging and versioning tools through MLflow. MLflow Tracing displays in-line traces directly in notebook results, allowing developers to see exactly how long each step took and inspect intermediate outputs like retrieved documents. 
# MAGIC
# MAGIC This is complemented by MLflow logging, which tracks and versioned agent code and configurations within Delta Tables to create a permanent, auditable record of every iteration. Together, these features provide a "single pane of glass" to quickly debug complex logic and identify the root causes of errors or performance bottlenecks.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Label Evaluation Datasets
# MAGIC
# MAGIC To accelerate the evaluation process, Databricks provides a research-backed API for generating high-quality synthetic data, which immediately unblocks quality assessments without requiring constant input from Subject Matter Experts (SMEs). The system focuses on efficiency by generating a "ground truth" list of facts instead of verbose written responses, making the review process significantly faster for SMEs. These easy-to-use tools allow teams to quickly validate synthetic data against existing benchmarks rather than starting from scratch, ensuring a streamlined path to reliable agent performance.