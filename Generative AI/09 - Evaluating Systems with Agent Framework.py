# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Evaluating Systems with Agent Framework
# MAGIC
# MAGIC After building the model, it is essential to evaluate its performance. In this demo, we will demonstrate how to use the **Agent Framework** to assess the model's performance. The example will show how to calculate built-in evaluation metrics and define custom metrics.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC *By the end of this demo, you will be able to:*
# MAGIC
# MAGIC * Load a model from the model registry for evaluation.
# MAGIC
# MAGIC * Identify common built-in evaluation metrics.
# MAGIC
# MAGIC * Define custom evaluation metrics.
# MAGIC
# MAGIC * Run an evaluation test and view the results using the UI or code.

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

# MAGIC %pip install -qq -U databricks-sdk databricks-langchain databricks-vectorsearch databricks-agents langchain==0.3.27 langchain-community==0.3.27 mlflow>=3.0 databricks-feature-engineering --upgrade
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
# MAGIC ## Prepare for Evaluation
# MAGIC
# MAGIC The first step is to load the model that will be used for evaluation. The RAG model we built in the previous demo was **registered in the UC model registry**.
# MAGIC
# MAGIC After loading the model, we will **define the evaluation dataset**. This dataset must include a **"request"** field to be used as the input query for the model. It typically also includes **"ground-truth" fields for response or context**. In this demo, to keep it simple, we will use only one request-response pair.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Load the Model
# MAGIC
# MAGIC Let's start by loading the model so that we can use it to generate responses and evaluate those responses later. Note that we will load a specific version of the model.

# COMMAND ----------

import mlflow
mlflow.set_registry_uri("databricks-uc")

model_uri = f"models:/{catalog_name}.{schema_name}.getstarted_genai_rag_demo/1"
print(model_uri)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Load Evaluation Dataset
# MAGIC
# MAGIC In this demo we will only use **"request" and "expected_response"**. For examples of using other fields, you can check [sample evaluation sets](https://docs.databricks.com/en/generative-ai/agent-evaluation/evaluation-set.html#sample-evaluations-sets). 
# MAGIC
# MAGIC Evaluation dataset is crucial for the accuracy of the evaluation. Some of the best practices are; 
# MAGIC * When developing an evaluation set, treat each sample as a unit test with a specific scenario and expected outcome, **including challenging examples and adversarial scenarios**. 
# MAGIC
# MAGIC * Ensure the evaluation set **reflects a variety of questions**, even beyond the application's primary domain, to prevent hallucinations or harmful responses. 
# MAGIC
# MAGIC * **High-quality, consistent human-generated labels are crucial**; achieve this by aggregating responses from multiple labelers and providing clear instructions to ensure consistency.

# COMMAND ----------

import pandas as pd

eval_set = pd.DataFrame([
    {
        "request": "personalized wooden name sign with app control",
        "expected_response": "Add a personal touch to your space with this handcrafted wooden name sign, perfect for nurseries, kids' rooms, weddings, or as a thoughtful gift. Made from high-quality wood, this custom sign is available in various sizes, fonts, and colors to suit your style. Lightweight and easy to install, it’s designed for durability and a smooth finish. Simply choose your size and color, enter the desired name or word, and let us create a unique piece just for you. Each sign is made to order with care, ensuring a timeless addition to your home or event decor.",
    }
])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Model Evaluation

# COMMAND ----------

# MAGIC %md
# MAGIC ### Build-in Metrics
# MAGIC
# MAGIC Mosaic AI Agent Framework uses LLM-judges to evaluate the model using common evaluation metrics such as safety and relevance. Also, it calculates system metrics such as token count and latency.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Custom Metric
# MAGIC
# MAGIC Although the Agents Evaluation framework automatically calculates common evaluation metrics, there are instances where we may need to assess the model using custom metrics. In this section, we will define a custom metric to evaluate whether the **response** generated is creative or not.

# COMMAND ----------

from mlflow.metrics.genai import make_genai_metric_from_prompt

# Define a custom assessment to detect PII in the retrieved chunks. 
creativity_prompt = "Your task is to determine whether generated product idea is creative or not. Grade idea from 1 to 5, 5 being very creative, 1 being very boring. This is the output: {response}."

creativity_level = make_genai_metric_from_prompt(
    name="creativity_level",
    judge_prompt=creativity_prompt,
    model="endpoints:/databricks-meta-llama-3-3-70b-instruct",
    metric_metadata={"assessment_type": "ANSWER"},
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run Evaluation Test
# MAGIC
# MAGIC Please note that in the code below, we are logging the evaluation process using MLflow to enable viewing the results through the MLflow UI.

# COMMAND ----------

print(model_uri)
with mlflow.start_run(run_name="rag_eval_demo_04_01"):
    eval_results = mlflow.evaluate(
        data=eval_set,
        model = model_uri,
        model_type = "databricks-agent",
        extra_metrics=[creativity_level]
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Review Evaluation Results
# MAGIC
# MAGIC We have two options for reviewing the evaluation results. The first option is to examine the metrics and tables directly using the results object. The second option is to review the results through the user interface (UI).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Review Results via the UI
# MAGIC
# MAGIC To view the results in the UI, follow these steps:
# MAGIC
# MAGIC - Click on the **"Experiment"** link displayed at the top of the previous code block's output for a simpler method.
# MAGIC
# MAGIC - Alternatively, you can navigate to "Experiments" in the left panel and locate the experiment registered with the title of this notebook.
# MAGIC
# MAGIC - View the overall metrics in the **Model Metrics** tab.
# MAGIC
# MAGIC - Examine detailed results for each assessment in the **Evaluation Results** tab.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Review Results Table

# COMMAND ----------

display(eval_results.metrics)

# COMMAND ----------

display(eval_results.tables['eval_results'])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Clean up Classroom
# MAGIC
# MAGIC **🚨 Warning:** Please refrain from deleting resources created in this demo, as they are required for upcoming demonstrations. To clean up the classroom assets, execute the classroom clean-up script provided in the final demo.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Summary
# MAGIC
# MAGIC In this demo, we demonstrated how to load a model from the model registry and evaluate its performance using both built-in metrics and custom metrics. As an example of a custom metric, we defined one that assesses the creativity of the generated response. After running the evaluation, we showed how to view the results using the MLflow UI and the result object table.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>