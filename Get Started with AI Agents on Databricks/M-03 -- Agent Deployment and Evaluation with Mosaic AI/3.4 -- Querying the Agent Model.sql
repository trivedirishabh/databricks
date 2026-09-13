-- Databricks notebook source
-- MAGIC %md
-- MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Demo - Querying the Agent Model
-- MAGIC Now that we have deployed our model to Databricks Model Serving, we can query the model.
-- MAGIC ### Learning Objectives
-- MAGIC _By the end of this demo, you will be able to:_ 
-- MAGIC - View a deployed model serving endpoint
-- MAGIC - Query a model serving endpoint using the UI
-- MAGIC - Query a model serving endpoint using SQL

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Querying an Agent Deployed to Mosaic AI Model Serving Using the UI
-- MAGIC The last cell in the `driver` notebook deployed our agent model to Databricks Model Serving. The deployment process takes about 10-12 minutes.
-- MAGIC
-- MAGIC #### Instructions
-- MAGIC 1. Navigate to **Serving** on the left side menu and click on the endpoint called `agents_dbacademy-get_started_agents-my_first_agent`.
-- MAGIC 1. Click on **Use** at the top right. 
-- MAGIC 1. Begin querying! Here are some examples of queries you can use: 
-- MAGIC     - _Get the order history of ronald54@example.net_
-- MAGIC     - _Can you tell me the policy for exchanging items?_
-- MAGIC
-- MAGIC > Please note: If you are using Databricks Free Edition, the endpoint may have scaled to zero. This means the query will take longer than normal.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Querying an Agent Deployed to Mosaic AI Model Serving Using SQL
-- MAGIC We can also query the model using SQL. We will use the built-in function, called [ai_query()](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_query) to query the model, passing the endpoint name as the first parameter.

-- COMMAND ----------

SELECT ai_query(
  'agents_dbacademy-get_started_agents-my_first_agent',
  '{"input": [{"role": "user", "content": "Can you tell me the policy for exchanging items?"}]}'
) AS Output