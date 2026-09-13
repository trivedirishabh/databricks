# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Introduction to Mosaic AI Model Serving

# COMMAND ----------

# MAGIC %md
# MAGIC ### Model Serving is Difficult
# MAGIC ![deploy-problems.png](./Includes/images/deploy-problems.png "deploy-problems.png")
# MAGIC The truth is the majority of models never make it to production. 
# MAGIC
# MAGIC We analyzed six key industries to better understand these trends by looking at the ratio of logged-to-registered models. What did we find? Our three most efficient industries put 25% of their models into production.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mosaic AI Model Serving
# MAGIC
# MAGIC ![deploy-solutions.png](./Includes/images/deploy-solutions.png "deploy-solutions.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Model Serving Modes
# MAGIC ![deploy-modes.png](./Includes/images/deploy-modes.png "deploy-modes.png")
# MAGIC There are four different modes that you can use to serve your models: batch, streaming, real-time and edge.
# MAGIC
# MAGIC - **Batch Inference**: great for high-latency scenarios. It leverages data saved in a database or object storage and allows for fast retrieval of stored predictions.
# MAGIC
# MAGIC - **Streaming Inference**: used for stream processing and used for scoring on new data. 
# MAGIC
# MAGIC - **Real-time Inference**: ideal for low-latency scoring and high availability. This mode usually uses REST protocol to serve models. Databricks model serving is a real-time inference options that allows low latency and highly available model inference.
# MAGIC
# MAGIC - **Embedded (edge) Inference**: a special case deployment that’s great for limited connectivity with cloud services.
# MAGIC
# MAGIC In this workflow, we now also introduce Agent Bricks, a new offering designed to let you build and deploy AI agent systems. While AI Builder operates at a higher abstraction layer, it still relies on the core capabilities shown here, registered models and scalable serving endpoints.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Model Serving on Databricks
# MAGIC ![model-serving-on-db.png](./Includes/images/model-serving-on-db.png "model-serving-on-db.png")
# MAGIC Since Databricks builds on top of MLflow, it inherits key components like model artifacts and tracking. Databricks takes this a step further via various automation processes and integrating key platform features like production-ready evaluation strategies and inference tables. Furthermore, serverless deployment allows for low latency and high throughput in a secure environment provided by Unity Catalog. 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Databricks Lakeflow Overview
# MAGIC Let’s take a look at how Lakeflow supports the end-to-end ML pipeline within the Databricks ecosystem.
# MAGIC
# MAGIC - **Lakeflow Connect**: provides high-performance ingestion connectors to bring raw data into the Lakehouse, this is critical for building robust feature sets.
# MAGIC
# MAGIC - **Lakeflow Spark Declarative Pipeliness**: plays a vital role in managing feature pipelines with reliable, scalable, and declarative ETL.
# MAGIC
# MAGIC - **Lakeflow Jobs**: automates feature engineering, triggers model training, and orchestrats model deployments.
# MAGIC
# MAGIC This unified stack is built on top of Apache Spark and Structured Streaming for performance and scale, with Unity Catalog ensuring secure access and governance across your data, models, and assets.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Databricks Lakeflow Jobs Features
# MAGIC ![lakeflow-jobs.png](./Includes/images/lakeflow-jobs.png "lakeflow-jobs.png")
# MAGIC Lakeflow Jobs offer a powerful and flexible way to automate ML pipelines across any cloud.
# MAGIC
# MAGIC With the Orchestrate Anything, Anywhere feature, we can automate key ML tasks like running notebooks for data processing, training models, refreshing feature tables, and more—across clouds and regions.
# MAGIC
# MAGIC It’s a fully managed orchestration layer, so you don’t need to worry about infrastructure. Just define your ML tasks, and Lakeflow Jobs will take care of running them reliably.
# MAGIC
# MAGIC And it’s simple to use, with an intuitive UI for both beginners and advanced users. Even complex pipelines involving CI/CD for model promotion can be built directly into the workflow system.
# MAGIC
# MAGIC This lets teams focus more on building and deploying models—and less on managing how they’re run.