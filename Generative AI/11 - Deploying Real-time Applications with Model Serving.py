# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # DEMO - Real-time Deployment with Model Serving
# MAGIC
# MAGIC In this demo, we will serve the model stored in the model registry using Mosaic Model Serving. We will utilize the Agent Framework to serve the models. When models are served with the Agent Framework, an app called Review App is automatically deployed alongside the model, allowing you to interact with the model and gather human feedback on its responses.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC *By the end of this demo, you will be able to:*
# MAGIC
# MAGIC - Deploy a model using the Agent Framework.
# MAGIC - Use the Review App to interact with the model and collect human feedback.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Important: Select Environment 4
# MAGIC The cells below may not work in other environments. To choose environment 4: 
# MAGIC 1. Click the ![environment.png](./Includes/images/environment.png "environment.png") button on the right sidebar
# MAGIC 1. Open the **Environment version** dropdown
# MAGIC 1. Select **4**

# COMMAND ----------

# MAGIC %md
# MAGIC ## Install Necessary Python Libraries
# MAGIC Run the next cell to install python libraries.
# MAGIC
# MAGIC >If you get anything that says "Note: you may need..." or if you see any other warnings, etc., you can generally disregard them in this environment.

# COMMAND ----------

# MAGIC %pip install -qq -U databricks-sdk databricks-langchain databricks-vectorsearch langchain==0.3.27 langchain-community==0.3.27 databricks-agents mlflow>=3.0 databricks-feature-engineering
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Classroom Setup
# MAGIC The following cell:
# MAGIC 1. Captures your username and creates an endpoint name based on that username
# MAGIC 1. Verifies that the **dbacademy** catalog and **get_started_genai** schema exist.
# MAGIC
# MAGIC >If you get any errors in the cell below, double-check that you have run all cells in the [00 - REQUIRED Initial Setup]($./00 - REQUIRED Initial Setup) notebook.

# COMMAND ----------

#############################################################################################
# Capture the username
username = dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
endpoint_name = f"{username}-model".replace('.', '-').replace('@', '-')
#############################################################################################

####################################################################################
# Set python variables for catalog, schema, and volume names (change, if desired)
catalog_name = "dbacademy"
schema_name = "get_started_genai"
####################################################################################

####################################################################################
# Create the catalog, schema, and volume if they don't exist already
spark.sql(f"USE CATALOG {catalog_name}")
spark.sql(f"USE SCHEMA {schema_name}")
####################################################################################

# COMMAND ----------

# MAGIC %md
# MAGIC ## Serve the Model with Mosaic AI Model Serving
# MAGIC
# MAGIC **Setting Up Model Serving**
# MAGIC
# MAGIC In order to keep it simple, in this demo, we are going to use the Mosaic AI Model Serving UI for creating, managing and using Model Serving endpoints. We can create model serving endpoints with the **"Serving"** page UI or directly from the registered **"Models"** page or from the **Catalog** Explorer.  
# MAGIC
# MAGIC Let's go through the steps of creating a model serving endpoint on the **Catalog** page. **You will not actually create the endpoint.**
# MAGIC
# MAGIC - Right-click **Catalog** in the left navigation, and select, "Open Link in New Tab". 
# MAGIC
# MAGIC - Select the **dbacademy** catalog and **get_started_genai** schema.
# MAGIC
# MAGIC - Select **Models** and then the **getstarted_genai_rag_demo** model.
# MAGIC
# MAGIC - Click the **Serve this model** button on the top right. This will take you to the **Serving endpoints** page.
# MAGIC
# MAGIC - Next in **General**, enter in a name of the form **firstName-lastName-endpoint**.
# MAGIC
# MAGIC - There are several configurations under **Served entities** that we will not discuss here. Leave **Entity**, **Compute type** and **Compute scale-out** to default values. You can select **Scale to zero** for this lesson as well. This feature can save costs by allowing the endpoint compute to shut down if there are no requests after a period of time. Databricks Free Edition requires this to be checked. 
# MAGIC
# MAGIC - **Do not click "Create"** at the bottom right. The above instructions are only for demonstration purposes. **You do not need to provision an endpoint because we already did so in the [00 - REQUIRED Initial Setup]($./00 - REQUIRED Initial Setup)** notebook.
# MAGIC
# MAGIC     - If you happen to accidentally create an endpoint, you can navigate to the left side bar and click on **Serving**. Then click on the endpoint you provisioned and click on the 3 vertical dots at the top right. Select **Delete**. Again, **Do not provision an endpoint.**

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query the Endpoint
# MAGIC
# MAGIC >Note: If you are using Databricks Free Edition, the endpoint has to have "scale to zero" enabled, which means the endpoint may have gone to sleep. If this is the case, it may take awhile for the query to execute. This is why "scale to zero" is not recommended for production use.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT ai_query(
# MAGIC   'daboncanplay-gmail-com-model',
# MAGIC   request => named_struct(
# MAGIC     'messages', array(
# MAGIC       named_struct(
# MAGIC         'role', 'user',
# MAGIC         'content', 'handmade lamp with remote control'
# MAGIC       )
# MAGIC     )
# MAGIC   )
# MAGIC ) AS Results

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC In this demo, we first deployed the registered model using the Agent Framework. Then, we interacted with the deployed model through the Review App.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>