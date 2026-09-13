# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Welcome to the Course!
# MAGIC ## Important Note:
# MAGIC This course will run in Databricks Free Edition. However, please note that, in the course notebooks, we will be deploying a model to Mosaic AI Model Serving. Databricks Free Edition has caps on the number of model serving endpoints you can deploy. If you run into errors in any of the notebooks that deploy this infrastructure, please double-check that you have not hit these caps.

# COMMAND ----------

# MAGIC %md
# MAGIC # Introduction to Machine Learning on Databricks

# COMMAND ----------

# MAGIC %md
# MAGIC ### Roles
# MAGIC ![ML_lifecycle.png](./Includes/images/ML_lifecycle.png "ML_lifecycle.png")
# MAGIC
# MAGIC The machine learning lifecycle is typically handled by entire teams composed of the following roles:
# MAGIC
# MAGIC - **Data governance officer**: establishes governance frameworks and collaborates with various departments to safeguard and manage data assets effectively.
# MAGIC
# MAGIC - **Data Engineers**: work on data pipelines, ETL processes, and ensure data is accessible, clean, and ready for analysis or machine learning.
# MAGIC
# MAGIC - **Data Scientists**: build and validate statistical models, conduct experiments, and often use machine learning to predict outcomes or optimize processes.
# MAGIC
# MAGIC - **Machine Learning Engineers**: work at the intersection of data engineering and software development to ensure models are efficient, scalable, and integrated into applications or Lakeflow Jobs.
# MAGIC
# MAGIC - **Business Stakeholders**: collaborate with data professionals to ensure analytics and models align with business goals and add value.
# MAGIC
# MAGIC >Note: there may also be other roles involved, like data analysts 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Processes
# MAGIC The machine learning lifecycle is made up of the following processes:
# MAGIC
# MAGIC - **Data Preparation**: clean and organize raw data for ML.
# MAGIC - **EDA**: summarize and visualize data to guide modeling.
# MAGIC - **Feature Engineering**: modify variables to improve models.
# MAGIC - **Model Training**: fit model to minimize errors.
# MAGIC - **Validation**: test model on holdout data.
# MAGIC - **Deployment**: move validated models to production; Databricks suggests deploying code for safer automation.
# MAGIC - **Monitoring**: track models for issues like drift.
# MAGIC
# MAGIC Databricks supports the entire ML lifecycle. This course covers EDA, feature engineering, training, validation, and deployment.
# MAGIC
# MAGIC >This is a beginning/introductory level course. For more, please see more advanced courses.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Machine Learning Lifecycle
# MAGIC Let’s first look at the role of Data Scientist. Starting from data preparation and featurization, using custom code, our data scientist is responsible for managing the pipeline. This includes EDA, baseline model testing, and other tasks that take place in the development environment. 
# MAGIC
# MAGIC Next, let’s look at our ML Engineer. The tasks of setting up webhooks and automated model testing typically belong to them. Mlflow, which we will discuss later, is used for model tracking, and Unity Catalog will be our model registry. For scheduling model retraining jobs, we use Databricks Lakeflow Jobs, which will also be discussed later. 
# MAGIC
# MAGIC A data engineer can then load the registered model and use it for batch or real-time inference, in addition to monitoring deployed models. 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Model Monitoring on Databricks
# MAGIC Let’s close out this introduction to machine learning with what is usually the last step in the overall process: model monitoring.
# MAGIC
# MAGIC Model monitoring is a key component of the ML process. Databricks supports both batch and streaming datasets and uses a data-centric approach to monitor model performance. As a machine learning practitioner, paying close attention to profile and drift metrics will be an important part of the monitoring process.
# MAGIC
# MAGIC Databricks offers a data-centric approach to model monitoring with auto-generated dashboards that can be used to check the overall health of your deployed models. Data Profile monitors include the following features:
# MAGIC
# MAGIC - Incrementally processes data in UC tables
# MAGIC - Calculates profile metrics and drift metrics
# MAGIC - Supports custom metrics as SQL expressions
# MAGIC - Auto-generates DBSQL dashboard for tracking drift, performance, and quality metrics over time.
# MAGIC - For MLOps, use in conjunction with inference tables to monitor models 
# MAGIC
# MAGIC
# MAGIC >Note: In this course, we only introduce you to monitoring, but more information is available [here](https://docs.databricks.com/aws/en/data-quality-monitoring/data-profiling/)