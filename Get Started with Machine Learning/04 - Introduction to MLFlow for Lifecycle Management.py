# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Introduction to MLFlow for Lifecycle Management

# COMMAND ----------

# MAGIC %md
# MAGIC ### MLFlow
# MAGIC ![mlflow.png](./Includes/images/mlflow.png "mlflow.png")
# MAGIC MLflow is an open-source platform designed for managing the end-to-end lifecycle of machine learning and was developed by Databricks. From preparing your raw data to deploying your models, Databricks is fully capable of handling every aspect of the ML lifecycle. MLflow consists of four main components: 
# MAGIC
# MAGIC - **Model tracking**: Record and query experiments including code, data, configuration, and results. 
# MAGIC
# MAGIC - **Projects**: MLflow provides a packaging format for reproducible runs on any platform. 
# MAGIC
# MAGIC - **Models**: MLflow offers a general model format compatible with various deployment tools. 
# MAGIC
# MAGIC - **Model registry**: MLflow is a centralized and collaborative solution for managing the entire model lifecycle. 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Databricks Model Registry
# MAGIC After tracking an ML experiment, the final model is typically preserved for future use, and this is where the **Model Registry** comes into play. 
# MAGIC
# MAGIC It serves as a collaborative and centralized hub for managing models. 
# MAGIC
# MAGIC Here are some key functionalities: 
# MAGIC
# MAGIC - version your ML artifacts
# MAGIC
# MAGIC - facilitate additional experimentation
# MAGIC
# MAGIC - integrate with approval and governance Lakeflow Jobs
# MAGIC
# MAGIC - audit any logs
# MAGIC
# MAGIC - automate with CI/CD integration. 
# MAGIC
# MAGIC Easily version your ML models and associated artifacts while testing to enable a smooth transition from one model stage to the next. All of this can be done through supportive CI/CD integration. 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Experiments
# MAGIC Tracking your experiments is made easier with the Databricks Experiments UI. 
# MAGIC
# MAGIC - Metadata Visibility: You can easily view metadata about experiments, such as the name, owner, creation date, and the last modification.
# MAGIC
# MAGIC - Experiment Management: The interface allows users to filter experiments and search by name or status, streamlining management.
# MAGIC
# MAGIC - Integrated Tracking System: Databricks integrates tracking for both traditional and AutoML models, simplifying experiment management in one platform.
# MAGIC
# MAGIC **MLflow Model Tracking** simplifies the process of monitoring and managing machine learning model development. It provides two tracking methods: 
# MAGIC
# MAGIC - manual logging for detailed custom tracking 
# MAGIC
# MAGIC - auto-logging for effortless monitoring 
# MAGIC
# MAGIC With just one line of code, you can keep tabs on various aspects of ML development, including: 
# MAGIC
# MAGIC - parameters
# MAGIC
# MAGIC - metrics
# MAGIC
# MAGIC - data lineage
# MAGIC
# MAGIC - models
# MAGIC
# MAGIC - the environment 
# MAGIC
# MAGIC Plus, all tracked information is packed in a standardized format, ensuring reproducibility throughout the development lifecycle.