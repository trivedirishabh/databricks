# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Lab - Creating Tools and Testing in the Playground
# MAGIC In this demo, you will explore how to create and register agent tools in Databricks to streamline customer service workflows. By combining structured tools (such as retrieving a customer’s interaction history) with unstructured tools (like searching product documentation through vector search), you will see how AI can automate common support tasks. The exercise walks you through building Unity Catalog functions, testing them in the AI Playground, and observing how different models leverage your tools to provide accurate, context-aware answers. 
# MAGIC
# MAGIC ### Learning Objectives
# MAGIC _By the end of this lab, you will be able to:_
# MAGIC - Create structured tools using Unity Catalog functions to retrieve customer interaction history.
# MAGIC - Build unstructured tools that leverage vector search for product documentation retrieval.
# MAGIC - Test and validate custom tools in Databricks SQL.
# MAGIC - Register and enable tools for use within the AI Playground.
# MAGIC - Interact with an AI agent that uses your tools to handle real-world customer service workflows.
# MAGIC - Compare model responses and (optionally) export your agent setup for deployment.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lab Scenario: Empowering Customer Service Representatives
# MAGIC
# MAGIC Customer service representatives at your company handle a high volume of support requests every day. To provide excellent service, they need to quickly review each customer’s past support history and access detailed product documentation to answer questions and resolve issues. However, searching for this information manually is time-consuming and can lead to delays or inconsistent answers. As a data and AI specialist, your goal is to empower the support team by building an intelligent agent that streamlines their workflow. This agent will allow customer service reps to instantly retrieve a customer’s interaction history and search product manuals for troubleshooting steps or technical details. By automating these tasks, you’ll help the team respond faster, improve accuracy, and deliver a better customer experience. In this lab, you’ll design, build, and test this AI-powered assistant using real customer service datasets and Databricks tools.

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
# MAGIC ## Create Structured and Unstructured Tools

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create a Structured Tool
# MAGIC
# MAGIC Create a Unity Catalog function to retrieve customer interaction history
# MAGIC 1. Create a function called `get_customer_interactions` that takes a customer email as input
# MAGIC 2. The function should return interaction details including date, issue category, and description
# MAGIC 3. Add proper comments to describe the function's purpose

# COMMAND ----------

spark.sql(f"""
---- TASK 1: Create a function to retrieve customer interaction history
---- There are multiple <FILL_IN> markings in the code below. These highlight the critical components of what are needed to create a SQL function. 
<FILL_IN> get_customer_interactions(
  customer_email <FILL_IN> 'Email address of the customer to retrieve interaction history for'
)
<FILL_IN> (
  interaction_date   DATE,
  issue_category     STRING,
  issue_description  STRING,
  customer_name      STRING
)
<FILL_IN> 'Retrieves interaction history for a specific customer including dates, categories, and descriptions'
LANGUAGE <FILL_IN>
<FILL_IN> (
  SELECT
    CAST(date_time AS DATE) as interaction_date,
    issue_category,
    issue_description,
    name as customer_name
  FROM {catalog_name}.{schema_name}.cust_service_data
  WHERE email = customer_email
  ORDER BY date_time DESC
  LIMIT 5
);
""")

# COMMAND ----------

# MAGIC %md
# MAGIC If you need help, the answer is in the next cell. Click the eyeball icon to expand the cell.

# COMMAND ----------

# MAGIC %skip
# MAGIC
# MAGIC spark.sql(f"""
# MAGIC ---- TASK 1: Create a function to retrieve customer interaction history
# MAGIC CREATE OR REPLACE FUNCTION get_customer_interactions(
# MAGIC   customer_email STRING COMMENT 'Email address of the customer to retrieve interaction history for'
# MAGIC )
# MAGIC RETURNS TABLE (
# MAGIC   interaction_date   DATE,
# MAGIC   issue_category     STRING,
# MAGIC   issue_description  STRING,
# MAGIC   customer_name      STRING
# MAGIC )
# MAGIC COMMENT 'Retrieves interaction history for a specific customer including dates, categories, and descriptions'
# MAGIC LANGUAGE SQL
# MAGIC RETURN (
# MAGIC   SELECT
# MAGIC     CAST(date_time AS DATE) as interaction_date,
# MAGIC     issue_category,
# MAGIC     issue_description,
# MAGIC     name as customer_name
# MAGIC   FROM {catalog_name}.{schema_name}.cust_service_data
# MAGIC   WHERE email = customer_email
# MAGIC   ORDER BY date_time DESC
# MAGIC   LIMIT 5
# MAGIC );
# MAGIC """)

# COMMAND ----------

# MAGIC %md
# MAGIC Let's test your structured tool:

# COMMAND ----------

# MAGIC %sql
# MAGIC ---- Test the customer interaction function
# MAGIC SELECT * FROM <FILL_IN>("nicolas.pelaez@example.com");

# COMMAND ----------

# MAGIC %md
# MAGIC If you need help, the answer is in the next cell. Click the eyeball icon to expand the cell.

# COMMAND ----------

# MAGIC %skip
# MAGIC %sql
# MAGIC -- Test the customer interaction function
# MAGIC SELECT * FROM get_customer_interactions("nicolas.pelaez@example.com");

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create an Unstructured Agent Tool
# MAGIC
# MAGIC Create a Unity Catalog function for product documentation search
# MAGIC 1. Create a function called `search_product_docs` that takes a search term as input
# MAGIC 2. The function should use vector search to find relevant product documentation
# MAGIC 3. Return the product name and documentation excerpt

# COMMAND ----------

spark.sql(f"""
---- TASK 2: Create a vector search function for product documentation
---- There are multiple <FILL_IN> markings in the code below. These highlight the critical components of what are needed to create a SQL function. 
<FILL_IN> search_product_docs(
  search_query STRING COMMENT 'Search term for finding relevant product documentation and troubleshooting guides'
)
<FILL_IN> (
  product_name STRING,
  doc_content  STRING
)
<FILL_IN> 'Searches product documentation using vector search to find relevant troubleshooting information'
<FILL_IN>(
  SELECT
    product_name,
    indexed_doc as doc_content
  FROM
    vector_search(
      <FILL_IN> => '{catalog_name}.{schema_name}.product_docs_index',
      <FILL_IN> => search_query,
      num_results => 2
    )
);
""")

# COMMAND ----------

# MAGIC %md
# MAGIC If you need help, the answer is in the next cell. Click the eyeball icon to expand the cell.

# COMMAND ----------

# MAGIC %skip
# MAGIC spark.sql(f"""
# MAGIC ---- TASK 2: Create a vector search function for product documentation
# MAGIC CREATE OR REPLACE FUNCTION search_product_docs(
# MAGIC   search_query STRING COMMENT 'Search term for finding relevant product documentation and troubleshooting guides'
# MAGIC )
# MAGIC RETURNS TABLE (
# MAGIC   product_name STRING,
# MAGIC   doc_content  STRING
# MAGIC )
# MAGIC COMMENT 'Searches product documentation using vector search to find relevant troubleshooting information'
# MAGIC RETURN(
# MAGIC   SELECT
# MAGIC     product_name,
# MAGIC     indexed_doc as doc_content
# MAGIC   FROM
# MAGIC     vector_search(
# MAGIC       index => '{catalog_name}.{schema_name}.product_docs_index',
# MAGIC       query_vector => ai_query("databricks-gte-large-en",search_query,"STRING")
# MAGIC     )
# MAGIC );
# MAGIC """)

# COMMAND ----------

# MAGIC %md
# MAGIC Let's test your unstructured search tool:

# COMMAND ----------

# MAGIC %sql
# MAGIC ---- Test the product documentation search
# MAGIC SELECT 
# MAGIC   product_name, 
# MAGIC   LEFT(doc_content, 200) as doc_preview
# MAGIC FROM <FILL_IN>('bluetooth headphone connection');

# COMMAND ----------

# MAGIC %md
# MAGIC If you need help, the answer is in the next cell. Click the eyeball icon to expand the cell.

# COMMAND ----------

# MAGIC %skip
# MAGIC %sql
# MAGIC ---- Test the product documentation search
# MAGIC SELECT 
# MAGIC   product_name, 
# MAGIC   LEFT(doc_content, 200) as doc_preview
# MAGIC FROM search_product_docs('bluetooth headphone connection');

# COMMAND ----------

# MAGIC %md
# MAGIC ## Enabling Tooling in AI Playground
# MAGIC Now we will enable tooling in the AI Playground.
# MAGIC ### 1. Open the AI Playground
# MAGIC
# MAGIC 1. In the left navigation, right-click **Playground**, and select "Open Link in New Tab".
# MAGIC 2. Select **Meta Llamma 3.3 70b Instruct**. Any model that has the "Tools enabled" icon can be used. 
# MAGIC
# MAGIC ### 2. Add Tools to Your Agent
# MAGIC After selecting your agent, you can now add a tool in the Playground. Here is an image for reference: 
# MAGIC
# MAGIC <img src="../../Includes/images/tool-select.png" alt="Tool Selection" width="600"/>
# MAGIC
# MAGIC
# MAGIC 1. In the **Tools** menu select **Add**. 
# MAGIC 1. Select **+ Add tool**.
# MAGIC 1. Under the  **UC Function** tab, click the dropdown menu labeled **Add hosted function**.
# MAGIC     - Select `dbacademy.get_started_agents.search_product_docs`
# MAGIC     - Click on **Save**.
# MAGIC     - Repeat for your other function
# MAGIC
# MAGIC 1. **Test the Functions**
# MAGIC    - In the chat window, type a prompt that would require the agent to use one or more of your tools.  
# MAGIC      Example prompts:
# MAGIC      - “Show me the latest customer return.”
# MAGIC      - “I want to return the product I purchased recently.”
# MAGIC    - The agent doesn't know your account, so it will ask for your email. Provide the email for `nicolas.pelaez@example.com` as an example. When asked about the product, use `bluetooth headphone` and it should return the right order.
# MAGIC    - Follow the conversation and see if you are eligible for return or not.
# MAGIC
# MAGIC 5. **Review the Output**
# MAGIC    - Check the agent’s response and verify that the output matches the expected results from your functions.
# MAGIC
# MAGIC 6. **Compare Model Responses (Optional)**
# MAGIC    - You can add multiple endpoints or models to compare how different LLMs use your tools. However, please note that Databricks Free Edition places caps on the number of queries to some models.
# MAGIC
# MAGIC 7. **Export Your Agent (Optional)**
# MAGIC    - After testing, you can export your agent setup to a Python notebook for further development or deployment.
# MAGIC    - Navigate to **Get code** at the top of the AI Playground. 
# MAGIC       1. Select **Create Agent Notebook**.
# MAGIC       1. This will open a new window showing you pre-generated Python code. 
# MAGIC       1. Inspect the notebook to see what the notebook accomplishes.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion 
# MAGIC You have now completed the process of building, testing, and registering agent tools in Databricks. Along the way, you created SQL functions, integrated them into the AI Playground, and validated their outputs against real-world customer service use cases. This hands-on workflow highlights how tool integration extends the power of large language models, transforming them into reliable, domain-specific assistants. Going forward, you can expand this foundation with additional functions, experiment with multiple models, and export your setup for deployment. With these skills, you're well equipped to design intelligent agents that deliver consistent and efficient results for your organization.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> |
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> |
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>