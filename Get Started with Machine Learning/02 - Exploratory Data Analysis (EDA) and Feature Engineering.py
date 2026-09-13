# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Exploratory Data Analysis (EDA) and Feature Engineering

# COMMAND ----------

# MAGIC %md
# MAGIC ### Databricks Data Intelligence Platform
# MAGIC ![DB-IP.png](./Includes/images/DB-IP.png "DB-IP.png")
# MAGIC
# MAGIC Databricks has built-in features that make your job much easier:
# MAGIC
# MAGIC - With Unity Catalog, you can search and find tables using your company’s natural language, even with large datasets.
# MAGIC
# MAGIC - Databricks’ Intelligence Engine (IE) understands your data and relationships to guide you to the right resources.
# MAGIC
# MAGIC - In Delta Lake, IE automates data optimization (like indexing and partitioning), so you don’t have to manage it manually.
# MAGIC
# MAGIC - For data warehousing, AI features like text-to-SQL let you write queries in plain language—Databricks generates the code for you, streamlining performance and efficiency.
# MAGIC For job orchestration, IE selects the right compute resources and start times, handling auto-scaling and automated error remediation.
# MAGIC
# MAGIC - IE also provides automatic data quality monitoring, detecting and flagging model quality issues and assisting with fixes.
# MAGIC
# MAGIC The platform supports building custom generative AI applications, with all features built for governance and powered by Delta Lake.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Delta Lake
# MAGIC ![delta-lake.png](./Includes/images/delta-lake.png "delta-lake.png")
# MAGIC
# MAGIC Delta Lake ensures high-quality, scalable, and efficient data management, which is crucial for creating robust machine learning models, especially in production environments. As an ML practitioner, you will consider key issues like:
# MAGIC
# MAGIC - Data reliability and integrity
# MAGIC
# MAGIC - Efficient data management
# MAGIC
# MAGIC - Scalability and performance
# MAGIC
# MAGIC - Streaming and batch Lakeflow Jobs
# MAGIC
# MAGIC - Data versioning and governance across multiple environments
# MAGIC
# MAGIC - Interoperability with ML pipelines
# MAGIC
# MAGIC While Delta Lake is an open-source format accessible to everyone, Databricks offers a fully managed solution that couples Delta Lake with its Machine Learning Runtime. This combination provides practitioners with powerful tools, optimized performance, and scalability, enabling them to focus more on model development and less on managing infrastructure.
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Pre-Built Infrastructure Management on Databricks
# MAGIC ![ml-infrastructure.png](./Includes/images/ml-infrastructure.png "ml-infrastructure.png")
# MAGIC
# MAGIC The Databricks ML runtime is a pre-built machine learning infrastructure that saves you time and offers top performance.
# MAGIC
# MAGIC Databricks provides one-click access to reliable and performant distribution of popular ML frameworks and simplifies scaling using an auto-scaling compute infrastructure. It’s in this way that ML teams can tackle both small and big data projects without worrying about infrastructure management.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mosaic AI
# MAGIC Finally, Mosaic AI unifies the data layer and ML platform. All data assets and artifacts, such as models and functions, are discoverable and governed in a single catalog. Using a single platform for data and models makes it possible to track lineage from the raw data to the production model. Built-in data and model monitoring saves quality metrics to tables that are also stored in the platform, making it easier to identify the root cause of model performance problems.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Feature Engineering
# MAGIC ![FEonDB.png](./Includes/images/FEonDB.png "FEonDB.png")
# MAGIC Machine learning uses existing data to build a model to predict future outcomes. In almost all cases, the raw data requires preprocessing and transformation before it can be used to build a model. This process is called feature engineering, and the outputs of this process are called features - the building blocks of the model.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Feature Store
# MAGIC ![FSonDB.png](./Includes/images/FSonDB.png "FSonDB.png")
# MAGIC
# MAGIC A feature store is a centralized repository that enables data scientists to find and share features and also ensures that the same code used to compute the feature values is used for model training and inference.
# MAGIC
# MAGIC The Databricks Feature Store solves two key challenges:
# MAGIC
# MAGIC - **Reusability and Discoverability**: It automatically tracks feature lineage, including data sources and code versions. This enables lineage-based search, saving data scientists time on manual feature engineering and preventing inconsistencies in feature creation. The integration with MLflow also tracks which models consume specific features, ensuring safe updates and deletions.
# MAGIC
# MAGIC - **Eliminating Online/Offline Skew**: With MLflow integration, feature lookup logic is packaged with the model, ensuring consistent feature usage between training and deployment. This simplifies the client, allowing feature updates without client changes, and avoids offline/online skew risks.
# MAGIC