# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Mosaic AI Vector Search
# MAGIC
# MAGIC Mosaic AI Vector Search is a serverless, high-performance vector database fully integrated into the Databricks Data Intelligence Platform, specifically designed to power Retrieval-Augmented Generation (RAG) and generative AI applications.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Vector Search Databases
# MAGIC
# MAGIC - **Vector Embedding**: Numerical representation of data (such as text, images, or audio) in a multi-dimensional space that captures its semantic meaning. In RAG architecture contextual information is stored in vectors.
# MAGIC
# MAGIC **Vector Databases**:
# MAGIC - Specialized, full-fledged databases for unstructured data 
# MAGIC     - Inherit database properties, i.e. Create-Read-Update-Delete (CRUD)
# MAGIC
# MAGIC - Speed up query search for the closest vectors
# MAGIC     - Uses vector search algorithms such as Approximate Nearest Neighbor (ANN)
# MAGIC     - Organize embeddings into indices
# MAGIC
# MAGIC - Designed for efficient storage of vectors utilized in generative AI applications, which rely on identifying documents or images with similarities. 
# MAGIC
# MAGIC - Provide a query interface that retrieves vectors most similar to a specified query vector.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Mosaic AI Vector Search
# MAGIC - Stores vector representation of your data, plus metadata
# MAGIC
# MAGIC - **Hybrid Search**: Combines semantic similarity with traditional keyword-based matching for more precise results.
# MAGIC
# MAGIC - Tightly integrated with your Lakehouse
# MAGIC
# MAGIC - Scalable, low latency production service with zero operational overhead
# MAGIC
# MAGIC - Supports ACLs using Unity Catalog integration
# MAGIC
# MAGIC - API for real-time similarity search
# MAGIC
# MAGIC - Query can include filters on metadata
# MAGIC
# MAGIC - REST API and Python client

# COMMAND ----------

# MAGIC %md
# MAGIC ## Three Methods of Generating Embeddings
# MAGIC - Method 1: Managed Embeddings 
# MAGIC
# MAGIC     - **Databricks computes** the embeddings for your data using a model you specify.
# MAGIC
# MAGIC     - The index **automatically syncs** with the Delta table as the source data is updated.
# MAGIC
# MAGIC - Method 2: Self-Managed Embeddings
# MAGIC
# MAGIC     - **You provide pre-calculated embeddings** in your Delta table.
# MAGIC
# MAGIC     - The index **automatically syncs** with the Delta table as it is updated - **you are responsible for generating embeddings**.
# MAGIC
# MAGIC - Method 3: Direct Access 
# MAGIC
# MAGIC     - **You manually update the index** using the REST API or Python SDK when embedding data changes.
# MAGIC
# MAGIC     - Requires **manual intervention** to maintain synchronization.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Set up Mosaic AI Vector Search
# MAGIC 1. Create a Vector Search Endpoint
# MAGIC
# MAGIC     - This is the **compute resource** associated with vector search.
# MAGIC
# MAGIC     - Endpoints scale automatically to support the size of the index or the number of concurrent requests.
# MAGIC
# MAGIC     - Support for multiple compute types.
# MAGIC
# MAGIC 2. Create a Model Serving Endpoint
# MAGIC
# MAGIC     - Create if you choose to have Databricks compute the embeddings.
# MAGIC
# MAGIC     - Model Serving supports embeddings via **Foundation Models APIs** (e.g., BGE), **external models**, and **custom models**.
# MAGIC
# MAGIC 3. Create a Vector Search Index
# MAGIC
# MAGIC     - Created and **auto-synced** from a Delta table.
# MAGIC
# MAGIC     - Optimized to provide real-time approximate nearest neighbor searches.
# MAGIC
# MAGIC     - Indexes appear in and are **governed by Unity Catalog**.
# MAGIC
# MAGIC     - Index level ACLs.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>