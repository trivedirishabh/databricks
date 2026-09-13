-- Databricks notebook source
-- MAGIC %md
-- MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # MLFlow for GenAI
-- MAGIC ![mlflow-genai.png](./Includes/images/mlflow-genai.png "mlflow-genai.png")
-- MAGIC
-- MAGIC MLflow is an open-source platform designed for managing the end-to-end lifecycle of machine learning. Developed by Databricks, it comes pre-installed on the Databricks Runtime for ML. MLflow consists of four main components: model tracking, projects, model packaging, and model registry.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## MLFlow Model Tracking
-- MAGIC - Record LLM parameters such as temperature and model configurations.
-- MAGIC
-- MAGIC     - Record experiment parameters. Capture everything from hyperparameters to intricate model configurations. It's your one-stop-shop for documenting the essence of each run.
-- MAGIC
-- MAGIC - Log metrics and compare them to get insights about the performance and accuracy of your models.
-- MAGIC
-- MAGIC     - MLflow simplifies metric logging. Log and compare metrics to measure your model's performance effectively.
-- MAGIC
-- MAGIC - Store and manage output artifacts such as visualization images and serialized models.
-- MAGIC
-- MAGIC     - Store and manage output artifacts. Models and insightful plots are neatly organized for your convenience.
-- MAGIC
-- MAGIC - Store model’s source code from each run.
-- MAGIC
-- MAGIC     - MLflow doesn't just track results. It encapsulates the entire essence of your experiments.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## MLFlow Model Tracing
-- MAGIC - MLflow Tracing allows logging, analyzing, and comparing traces across different versions of Gen AI applications.
-- MAGIC
-- MAGIC - It allows debugging apps and keeping track of inputs and responses of Gen AI applications.
-- MAGIC
-- MAGIC - Benefits:
-- MAGIC     - Interactive trace visualizations.
-- MAGIC     - Track the latency impact of different frameworks, models, chunk size, etc.
-- MAGIC     - Measure cost by tracking token usage.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## MLFlow Model "Flavor"
-- MAGIC In MLflow, a flavor acts as a "universal adapter" that bridges the gap between specialized generative AI frameworks—like LangChain, Hugging Face, or OpenAI—and a standardized deployment environment. In the context of GenAI, a flavor essentially wraps a complex chain, agent, or model into a consistent format that MLflow understands. This abstraction allows you to log an intricate GenAI workflow (complete with its prompt templates, retrieval logic, and model parameters) and later load it back as a simple Python function (pyfunc). By doing so, MLflow ensures that the exact same logic used during experimentation can be deployed to a production server without needing to manually rewrite the interface for each different library.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Unity Catalog Model Registry
-- MAGIC - Model lifecycle management with versioning & @aliases.
-- MAGIC
-- MAGIC     - Aliases like **@champion** or **@challenger** allow downstream applications to always call the best model without changing underlying code.
-- MAGIC
-- MAGIC - Run Predictions
-- MAGIC
-- MAGIC     - Once you have a custom model registered in Unity Catalog, you can load it into a notebook and run **predict()**. This uses your notebook's attached compute.
-- MAGIC
-- MAGIC - Deploy models
-- MAGIC
-- MAGIC     - If you need a more scalable solution, you can deploy the model as a REST API by creating a Mosaic AI Model Serving endpoint directly from the Catalog Explorer or via the **databricks.agents** API for more complex agentic workflows.
-- MAGIC
-- MAGIC - Collaboration and ACLs
-- MAGIC
-- MAGIC     - In Unity Catalog, generative AI models enjoy first-class status by being treated as native, governed assets just like tables or volumes, which allows them to inherit the same robust security, lineage, and auditing controls as your data.
-- MAGIC
-- MAGIC - Tagging and annotations
-- MAGIC
-- MAGIC     - Add rich tagging and annotations to every model, ensuring that compliance and governance teams have all the necessary metadata for auditing.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>