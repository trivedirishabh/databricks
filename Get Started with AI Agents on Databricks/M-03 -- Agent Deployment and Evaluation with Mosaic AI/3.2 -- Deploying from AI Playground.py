# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Deploying from AI Playground
# MAGIC In this demo, you will learn how to move from rapid prototyping in the AI Playground to a fully deployed agent in Databricks. Starting with an exported Playground notebook, you’ll build an agent that can call Unity Catalog functions and vector search endpoints, test its responses, evaluate its performance with MLflow's GenAI Evaluation tools, and deploy it for production use. This process demonstrates the full lifecycle of an AI agent—-from experimentation to deployment—-showing how Databricks unifies tool creation, testing, evaluation, and deployment into a single streamlined workflow.
# MAGIC
# MAGIC ### Learning Objectives
# MAGIC _By the end of this demo, you will be able to:_ 
# MAGIC - Inspect Unity Catalog and workspace assets that power agent tooling
# MAGIC - Understand and modify a Playground-exported agent notebook
# MAGIC - Build a tool-calling agent with MLflow's `ResponsesAgent`
# MAGIC - Manually test and evaluate the agent using MLflow Trace UI - and Mosaic AI Evaluation
# MAGIC - Log and register the agent to Unity Catalog for governance and reproducibility

# COMMAND ----------

# MAGIC %md
# MAGIC ## Demo Scenario
# MAGIC
# MAGIC You are building an intelligent customer service agent for an e-commerce company. The agent needs to handle customer inquiries about returns, refunds, and product support. To make the agent effective, you'll create specialized tools that can:
# MAGIC
# MAGIC - Access customer service data to retrieve recent return requests
# MAGIC - Look up company policies to ensure compliance with business rules
# MAGIC - Review customer order history to determine eligibility for returns
# MAGIC - Search product documentation to provide technical support
# MAGIC
# MAGIC This scenario demonstrates how to combine structured data queries with unstructured document search to create a comprehensive customer service solution using Unity Catalog functions as agent tools.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Important: Select Environment 4
# MAGIC The cells below may not work in other environments. To choose environment 4: 
# MAGIC 1. Click the ![environment.png](../../Includes/images/environment.png "environment.png") button on the right sidebar
# MAGIC 1. Open the **Environment version** dropdown
# MAGIC 1. Select **4**

# COMMAND ----------

# MAGIC %md
# MAGIC ## REQUIRED - Setting required variables
# MAGIC
# MAGIC Run the following cell to configure some python variables we will be using in the rest of the notebook

# COMMAND ----------

####################################################################################
# Set python variables for catalog, schema, and volume names (change, if desired)
catalog_name = "dbacademy"
schema_name = "get_started_agents"
volume_name = "customer_service"
####################################################################################

# COMMAND ----------

# MAGIC %md
# MAGIC ## Inspecting UC & Workspace Assets
# MAGIC
# MAGIC #### Unity Catalog Assets
# MAGIC As a part of the first few lessons, we created multiple functions. Click on the **Catalog** on the left menu and navigate to dbacademy.get_started_agents. In the schema you will find four functions that have been created. Here is a summary of those SQL functions:
# MAGIC
# MAGIC 1. `get_latest_return`: Returns the most recent customer service interaction, such as returns.
# MAGIC 1. `get_order_history`: This takes the user_name of a customer as an input and returns the number of returns and the issue category
# MAGIC 1. `get_return_policy`: Returns the details of the Return Policy
# MAGIC 1. `search_product_docs`: Searches product documentation using vector search to retrieve relevant documentation excerpts for troubleshooting and support. This should be used to search by product as each product has its own documentation.
# MAGIC
# MAGIC #### Workspace Assets
# MAGIC - As a part of this course, we created a **standard vector search endpoint**.
# MAGIC
# MAGIC > This course does not go into detail on deploying a vector search endpoint. Please see our [other](https://www.databricks.com/training/catalog?search=generative+ai+solution+development) course offerings on this topic.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exporting Your Own Agent Notebook
# MAGIC Now that you have enabled an agent to use tools from Unity Catalog, you can export a notebook and begin developing in your own environment using the notebook as a template.  
# MAGIC  
# MAGIC ### Instructions
# MAGIC 1. After completing all the tasks in [Building and Prototyping Agent Tools with AI Playground]($../M-02 -- Building AI Agents on Databricks/2.3 -- Building and Prototyping Agent Tools with AI Playground), click **Get code** at the top of the AI Playground. 
# MAGIC 1. Select **Create Agent Notebook**.
# MAGIC
# MAGIC This will open a new window showing you pre-generated Python code in a Databricks notebook. The notebook has been placed in a new folder in your workspace with path **Workspace/Users/YOUR-USERNAME/new_agent_code_folder**.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Inspecting and Understanding the Contents of an Agent Notebook from Playground
# MAGIC
# MAGIC The notebook we just created builds a tool-calling agent on Databricks using MLflow's `ResponsesAgent`. It shows the full lifecycle:
# MAGIC - Author an agent that can call tools (Unity Catalog functions, optional Vector Search retrievers) via an OpenAI-compatible endpoint hosted by Databricks.
# MAGIC - Manually test the agent (predict + streaming).
# MAGIC - Evaluate the agent with MLflow GenAI Evaluation scorers.
# MAGIC - Log the agent to MLflow with required workspace resources.
# MAGIC - Register to Unity Catalog.
# MAGIC - Deploy the agent with `databricks.agents`. 
# MAGIC
# MAGIC ### Instructions
# MAGIC
# MAGIC Let's first add some evaluation prompts that we will discuss later.
# MAGIC
# MAGIC 1. Change the following text in cell 7:
# MAGIC
# MAGIC - "what is 4*3 in python" -> "Can you tell me the policy for exchanging items?"
# MAGIC
# MAGIC 2. Change the following text in both cells 10 and 12:
# MAGIC
# MAGIC - "What is an LLM agent?" -> "Can you tell me the policy for exchanging items?"
# MAGIC
# MAGIC We also need to add a catalog, schema, and model name to the generated notebook and set the model serving endpoint to "scale to zero".
# MAGIC
# MAGIC 3. Scroll down to cell 16, or alternatively, do a find for "TODO: define the catalog, schema, and model name for your UC model"
# MAGIC
# MAGIC 4. Add the following
# MAGIC
# MAGIC - For **catalog**, "dbacademy"
# MAGIC - For **schema**, "get_started_agents"
# MAGIC - For **model_name**, "my_first_agent"
# MAGIC
# MAGIC 5. Scroll to cell 18, or search for "agents.deploy(UC_MODEL_NAME, uc_registered_model_info.version, tags = {"endpointSource": "playground"})"
# MAGIC
# MAGIC When working with Databricks Free Edition, we need to allow the endpoint to scale to zero.
# MAGIC
# MAGIC 6. Paste the following as the last parameter in the function call on line 5, ", scale_to_zero=True". The completed function call should like this: 
# MAGIC
# MAGIC     `agents.deploy(UC_MODEL_NAME, uc_registered_model_info.version, tags = {"endpointSource": "playground"}, scale_to_zero=True)`
# MAGIC
# MAGIC 7. Click the **Run all** button at the top right of the notebook. 
# MAGIC
# MAGIC The last cell in the notebook deploys our model to Databricks Model Serving. If you get an error, you may have hit the cap for the number of model serving endpoints you can deploy in your workspace. The endpoint will take about 10-12 minutes to deploy. We will use the endpoint later in the course.
# MAGIC
# MAGIC > Note: once you run this notebook, you will find an additional `.py` file called `agent.py`. This is created via the `driver` notebook.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Agent Evaluation, MLflow, and Your UC-Registered Agent
# MAGIC While waiting for our model serving endpoint to deploy, let's view the test and evaluation output. Use the table of contents icon on the left side menu and navigate to **Test the agent**.
# MAGIC
# MAGIC The output for **cell 12** also shows the trace breakdown, input/output prompts, attributes, events, and assessments as a part of the evaluation process. Notice that the assessment shows the rationale behind the Feedback assessment . The screenshot below shows a typical output. 
# MAGIC
# MAGIC
# MAGIC <img src="../../Includes/images/mosaic-ai-framework.png" width="1000"/>
# MAGIC
# MAGIC
# MAGIC Click on one of the completions and take a look at some of the thoughts being used in the chat tab. For example, in the screenshot below we see that in the first completion, the assistant chose to search for relevant product documentation.
# MAGIC
# MAGIC
# MAGIC <img src="../../Includes/images/mosaic-ai-framework2.png" width="500"/>
# MAGIC
# MAGIC
# MAGIC Let's view the evaluation output. Use the table of contents icon on the left side menu and navigate to **Evaluate the agent with Agent Evaluation**. As a part of the output, there will be a blue button that says **View evaluation results**. Click on it. This will open a new window within Databricks that shows the evaluation results within MLflow. Explore the outputs there and navigate back to the `driver` notebook.
# MAGIC
# MAGIC > This course does _not_ perform a deep dive on MLflow. Please see the course [Generative AI Application Evaluation and Governance](https://www.databricks.com/training/catalog/generative-ai-application-evaluation-and-governance-2668) for further training on this topic. 
# MAGIC
# MAGIC This notebook also performs a pre-deployment validation step with sample input data in cell 14, which is best practice before registering to Unity Catalog. 
# MAGIC
# MAGIC In cell 16, our (agent) model is registered to Unity Catalog in the location we specified earlier. If you navigate there using the **Catalog** menu, you will see the model.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC You have now completed the journey from Playground experimentation to agent deployment. Along the way, you explored Unity Catalog functions, tested agent behavior, and applied evaluation tools to measure quality. Finally, you registered and deployed your agent, making it accessible and reusable within Databricks. These steps illustrate how Databricks supports the entire agent development lifecycle by bridging experimentation, evaluation, and deployment.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> |
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> |
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>