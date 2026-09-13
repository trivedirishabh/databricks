# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # Getting Started with Mosaic AI Model Serving
# MAGIC
# MAGIC In this lesson, we will focus on how to serve a registered model using **Mosaic AI Model Serving** for real-time inferencing. We’ll also introduce **Databricks Workflows** as a way to automate ML pipelines.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC By the end of this demo, you will be able to:
# MAGIC
# MAGIC 1. **Serve your model with Mosaic AI Model Serving**
# MAGIC     - Use the UI to serve your model.
# MAGIC     - Query the endpoint using the UI.
# MAGIC     - Explore the metrics and logs using the built-in dashboard.
# MAGIC
# MAGIC 2. **Introduction to ML With Workflows:**
# MAGIC     - Use the UI to demonstrate notebook automation for ML tasks via Databricks Workflows.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Important: Select Environment 4
# MAGIC The cells below may not work in other environments. To choose environment 4: 
# MAGIC 1. Click the ![environment.png](../Includes/images/environment.png "environment.png") button on the right sidebar
# MAGIC 1. Open the **Environment version** dropdown
# MAGIC 1. Select **4**

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Requirements
# MAGIC Ensure you have completed all tasks in the previous notebooks.
# MAGIC
# MAGIC The next cell will create some python variables that will be used in the notebook.

# COMMAND ----------

####################################################################################
# Set python variables for catalog and schema
catalog_name = "dbacademy"
schema_name = "get_started_ml"
# Capture username
username = dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
endpoint_name = f"{username}-model".replace('.', '-').replace('@', '-')
####################################################################################

# COMMAND ----------

# MAGIC %md
# MAGIC **Note🚨 : Please ensure you have completed the previous two demos.**

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Part 1: Mosaic AI Model Serving
# MAGIC
# MAGIC **Setting Up Model Serving**
# MAGIC
# MAGIC We can create Model Serving endpoints with the Databricks Machine Learning API or the Databricks Machine Learning UI. An endpoint can serve any registered Python MLflow model in the **Model Registry**.
# MAGIC
# MAGIC In order to keep it simple, in this demo, we are going to use the Model Serving UI for creating, managing and using the Model Serving endpoints. We can create model serving endpoints with the **"Serving"** page UI or directly from the registered **"Models"** page.  
# MAGIC
# MAGIC Let's go through the steps of creating a model serving endpoint on the Models page. **You will not actually create the endpoint.**
# MAGIC
# MAGIC - Right-click **Models** in the left navigation, and select, "Open Link in New Tab". 
# MAGIC
# MAGIC - Select **Owned by me**.
# MAGIC
# MAGIC - Select the model you want to serve under the **Name** column. Notice this will take you to the Catalog menu. 
# MAGIC
# MAGIC - Click the **Serve this model** button on the top right. This will take you to the **Serving endpoints** screen.
# MAGIC
# MAGIC - Next in **General**, enter in a name of the form **firstName-lastName-endpoint**.
# MAGIC
# MAGIC - There are several configurations under **Served entities** that we will not discuss here. Leave **Entity**, **Compute type** and **Compute scale-out** to default values. You can select **Scale to zero** for this lesson as well. This feature can save costs by allowing the endpoint compute to shut down if there are no requests after a period of time. Databricks Free Edition requires this to be checked. 
# MAGIC
# MAGIC - **Do not click "Create"** at the bottom right. The above instructions are only for demonstration purposes. **You do not need to provision an endpoint because we already did so in the last demo.**
# MAGIC
# MAGIC     - If you happen to accidentally create an endpoint, you can navigate to the left side bar and click on **Serving**. Then click on the endpoint you provisioned and click on the 3 vertical dots at the top right. Select **Delete**. Again, **Do not provision an endpoint.**

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Model Serving Endpoint with Python
# MAGIC
# MAGIC In the last demo, we used code very similar to this to create a Mosaic AI Model Serving Endpoint.

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC
# MAGIC from mlflow.deployments import get_deploy_client
# MAGIC
# MAGIC client = get_deploy_client("databricks")
# MAGIC endpoint_name = f"{username}-model"
# MAGIC endpoint_name = endpoint_name.replace("@databricks.com", "").replace('.', '-')
# MAGIC
# MAGIC # Check if the endpoint already exists
# MAGIC try:
# MAGIC     # Attempt to get the endpoint
# MAGIC     existing_endpoint = client.get_endpoint(endpoint_name)
# MAGIC     print(f"Endpoint '{endpoint_name}' already exists.")
# MAGIC except Exception as e:
# MAGIC     # If not found, create the endpoint
# MAGIC     if "RESOURCE_DOES_NOT_EXIST" in str(e):
# MAGIC         print(f"Creating a new endpoint: {endpoint_name}")
# MAGIC         endpoint = client.create_endpoint(
# MAGIC             name=endpoint_name,
# MAGIC             config={
# MAGIC                 "served_entities": [
# MAGIC                     {
# MAGIC                         "name": "my-model",
# MAGIC                         "entity_name": model_name,
# MAGIC                         "entity_version": "1",
# MAGIC                         "workload_size": "Small",
# MAGIC                         "scale_to_zero_enabled": True
# MAGIC                     }
# MAGIC                 ],
# MAGIC                 "traffic_config": {
# MAGIC                     "routes": [
# MAGIC                         {
# MAGIC                             "served_model_name": "my-model",
# MAGIC                             "traffic_percentage": 100
# MAGIC                         }
# MAGIC                     ]
# MAGIC                 }
# MAGIC             }
# MAGIC         )
# MAGIC     else:
# MAGIC         print(f"An error occurred: {e}")
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query Serving Endpoint
# MAGIC
# MAGIC Let's use the deployed model for real-time inference. Here’s a step-by-step guide for querying an endpoint in Databricks Model Serving:
# MAGIC
# MAGIC - Right-click on **Serving** in the left navigation and select, "Open Link in New Tab".
# MAGIC
# MAGIC - Select the endpoint you want to query. The one we created in the last demo is named "<your-user-name>-model". Please note that it is possible that the endpoint has not finished the setup process, which takes 10-12 minutes from the time we ran the last demo.
# MAGIC
# MAGIC - Click **Use** button the top right corner.
# MAGIC
# MAGIC - There are 4 methods for querying an endpoint; **browser**, **CURL**, **Python**, and **SQL**. For now, let's use the easiest method; querying right in the **browser** window. In this method, we need to provide the input parameters in JSON format. Since we used `mlflow.sklearn.autolog()` with `log_input_examples = True`, we registered an example with MLflow, which appears automatically when selecting **browser**.
# MAGIC
# MAGIC - Click **Send request**.
# MAGIC
# MAGIC - **Response** field on the right panel will show the result of the inference.
# MAGIC
# MAGIC > Please note: Since we enabled "Scale to zero", it is possible that our request takes longer than normal. Scale to zero is not recommended for production use because of the possibility of this delay.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT ai_query('daboncanplay-gmail-com-model',
# MAGIC     request => named_struct("wine_id",722,"fixed_acidity",6.8, "volatile_acidity",0.64, "citric_acid",0.0,"pH",3.44,"sulphates",0.63,"alcohol",11.3,"pHCategory",2.0), 
# MAGIC     returnType => 'DOUBLE') as prediction

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: ML With Workflows
# MAGIC
# MAGIC ### Creating a Job
# MAGIC
# MAGIC Now, let's create a workflow job to run this notebook:
# MAGIC
# MAGIC 1. Start by navigating to **Jobs & Pipelines** on the left sidebar.
# MAGIC
# MAGIC 2. You have 2 options to proceed:
# MAGIC
# MAGIC     Option 1: Navigate to the **Job Runs** tab, then click **Create Job** at the top-right corner.
# MAGIC
# MAGIC     Option 2: In the **Jobs and Pipelines** section, click the **Create** dropdown at the top-right corner, and select **Job** from the options.
# MAGIC
# MAGIC **Note:** Please make sure Lakeflow Pipelines Editor is turned **ON**.
# MAGIC
# MAGIC 3. Click on **Notebook**.   
# MAGIC
# MAGIC 3. In the presented menu, enter a name under **Task Name**. For example, you can use **test_task_name**.
# MAGIC
# MAGIC 4. Under **Type**, ensure that **Notebook** is selected. Also, make sure **Workspace** is selected under **Source**. Both should be selected by default.
# MAGIC
# MAGIC 5. Next, we will attach this notebook to the job. Go to **Path**. Click the drop-down menu. You will be presented with a menu that will allow you to navigate to this notebook. By default, you will already be in your home folder. Navigate to the course materials folder. Select `07 - Getting Started with Mosaic AI Model Serving`. Click **Confirm** at the bottom right of the **Select Notebook** menu. 
# MAGIC
# MAGIC 6. Under **Compute**, you'll see **Serverless** is automatically selected.
# MAGIC Use the drop-down menu to select your existing All-Purpose **cluster**.
# MAGIC
# MAGIC 7. You’ll see additional options, such as **dependent libraries**, **parameters**, **notifications**, **retries**, and **Metric threshold**. You can leave these options unpopulated for this lesson. 
# MAGIC
# MAGIC 8. Click **Create Task**. A message will appear at the top right indicating your task was successfully created.
# MAGIC
# MAGIC 9. In the right menu, there are various options. For example, you can add tags, set job parameters, and configure schedules for runs. We'll leave these alone for this lesson.
# MAGIC
# MAGIC 10. Finally, to give the job a name, double-click the title at the top left and enter an appropriate name. For example, `Workflow1`.
# MAGIC
# MAGIC 11. When you are ready to run the job, click **Run Now** at the top right. A note will appear at the top right indicating a run has been initiated. Note that due to the clean-up in the next cell, your data assets will be missing when inspecting your catalog after the job finishes. 
# MAGIC
# MAGIC ### Inspect Your Run
# MAGIC
# MAGIC After your job completes its run, you can inspect it:
# MAGIC
# MAGIC 1. Select **Jobs & Pipelines** again on the sidebar menu. 
# MAGIC
# MAGIC 1. Click on the name of the job you just created. 
# MAGIC
# MAGIC 1. There are a few ways to view the notebook you just ran. You can do any of the following and it will take you to the same location:
# MAGIC     - Click on **go to the latest successful run**.
# MAGIC     - Click on the date under **Start time**.
# MAGIC     - Click on the green bar (meaning a successful run) displayed within the diagram. If the bar is red, that means your job failed, but you can still inspect the notebook that ran. This option will also display the workflow configuration you setup previously. 
# MAGIC
# MAGIC 1. This will take you to a static copy of the notebook. You cannot edit it, but you can view the outputs of each cell. Confirm that all cells have run successfully. 
# MAGIC
# MAGIC Of course, this is a simple example of creating a job with a single notebook. In practice, we use the various options mentioned earlier to tie together complex pipelines.

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusion And Next Steps
# MAGIC
# MAGIC In this demo, you learned how to use **Mosaic AI Model Serving** for real-time inference with a registered model. You also explored **Databricks Workflows** as a way to schedule and automate ML jobs.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>