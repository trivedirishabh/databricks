# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Building and Prototyping Agent Tools with AI Playground
# MAGIC
# MAGIC In this demo, you'll learn how to create custom tools for AI agents using Unity Catalog functions. You will build functions that can serve as tools for intelligent customer service agents, and test them to ensure they work properly.
# MAGIC ### Learning Objectives
# MAGIC _By the end of this demo, you will be able to:_
# MAGIC - Create a Unity Catalog (UC) SQL function.
# MAGIC   - Define input, output, and descriptions for tools for agentic use cases.
# MAGIC - Use the Notebook for preliminary testing of UC functions and the Playground for agentic testing.

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
# MAGIC
# MAGIC 🚨 **Note**: If you have not done so, please complete **[Setting Up the Workspace]($../M-01 - Introduction to AI Agents on Databricks/1.3 -- Setting Up the Workspace)**. The setup notebook is required before we continue with the current notebook.

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
# MAGIC ## A. Explore the Dataset.
# MAGIC
# MAGIC This demonstration will focus on the dataset **cust_service_data** (located in schema **dbacademy.get_started_agents**)  and creating a SQL function an Agent can use with this dataset. Run the next cell to see the Delta table **cust_service_data**.
# MAGIC
# MAGIC 🚨 **Note**: If you have not done so, please complete **[Setting Up the Workspace]($../M-01 - Introduction to AI Agents on Databricks/1.3 -- Setting Up the Workspace)**. You will not be able to run this notebook without first setting up the workspace.

# COMMAND ----------

spark.sql(f"SELECT * FROM {catalog_name}.{schema_name}.cust_service_data").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. How To Create Structured SQL Functions as Agent Tools
# MAGIC Now that we understand how our data looks, let's create some useful tools needed for our agent that can be used with these datasets. When creating tools for agents, you will use various tool types. 
# MAGIC
# MAGIC Common types of agent tools include:
# MAGIC - **Structured data retrieval tools**: Query structured data sources like SQL tables.
# MAGIC - **Unstructured data retrieval tools**: Query unstructured data sources like document collections to perform retrieval augmented generation.
# MAGIC - **Custom tools**: Custom Python code that can be used by the agent. A simple example would be a function that returns today's date.
# MAGIC - **Code interpreter tools**: Allow agents to run arbitrary Python code.
# MAGIC - **External connection tools**: Connect to external services and APIs to fetch data or perform tasks.
# MAGIC
# MAGIC In this section, we will start by creating two tools: **structured** and **unstructured data retrieval** tools. Each tool (written in SQL) will have a specific purpose in helping with customer requests. The other tools mentioned above are outside the scope of this course. 
# MAGIC
# MAGIC 🚨 **Note**: We will be writing our tools to the **get_started_agents** schema in the **dbacademy** catalog.

# COMMAND ----------

# MAGIC %md
# MAGIC ### B1. Adding a Structured Data Retrieval Tool 
# MAGIC #### Get Latest Return in the Queue
# MAGIC
# MAGIC Let's create a function that identifies and retrieves the most recent return request from the ticketing or returns system. To demonstrate the syntax used for creating a function for structured data, let's breakdown the next cell line by line to better understand what is happening with the query. 
# MAGIC
# MAGIC **Note**: the SQL query that creates the function is encapsulated in a call to `spark.sql`. This is so we can use variables that represent the catalog and schema.
# MAGIC
# MAGIC - `CREATE OR REPLACE FUNCTION get_latest_return()`: This line defines a new function called `get_latest_return`. If an existing function with this name already exists, it will be replaced. No arguments are required to call this function—a key sign it's intended as a simple lookup.
# MAGIC - `RETURNS TABLE(
# MAGIC   purchase_date DATE, issue_category STRING, issue_description STRING, name STRING
# MAGIC )`: This statement tells us the function will output a table. Instead of a single value, it returns one or more rows—each with a fixed set of columns, described next.
# MAGIC - `COMMENT 'Returns the most recent customer service interaction, such as returns.'`: This adds a helpful comment to the function's definition—anyone using this function in the future can see at a glance what its main purpose is.
# MAGIC - `RETURN (
# MAGIC   SELECT 
# MAGIC     CAST(date_time AS DATE) AS purchase_date,
# MAGIC     issue_category,
# MAGIC     issue_description,
# MAGIC     name
# MAGIC   FROM cust_service_data
# MAGIC   ORDER BY date_time DESC
# MAGIC   LIMIT 1
# MAGIC )`: Begins the SQL statement that the function executes. This is the query whose output becomes the function's result.

# COMMAND ----------

spark.sql(f"""
-- Create a function to get the latest return request
CREATE OR REPLACE FUNCTION {catalog_name}.{schema_name}.get_latest_return()
RETURNS TABLE(
  purchase_date DATE, issue_category STRING, issue_description STRING, name STRING
)
COMMENT 'Returns the most recent customer service interaction, such as returns.'
RETURN (
  SELECT 
    CAST(date_time AS DATE) AS purchase_date,
    issue_category,
    issue_description,
    name
  FROM {catalog_name}.{schema_name}.cust_service_data
  WHERE issue_category = 'Returns'
  ORDER BY date_time DESC
  LIMIT 5
);
""")

# COMMAND ----------

# MAGIC %md
# MAGIC 1. Let's run a quick test on our function (which is really just a SQL query). Notice the syntax here is to call the function as `FROM <function_name>()`.

# COMMAND ----------

spark.sql(f"""
SELECT * 
FROM {catalog_name}.{schema_name}.get_latest_return();
""").display()   

# COMMAND ----------

# MAGIC %md
# MAGIC ### B2. Adding an Unstructured Data Retrieval tool
# MAGIC #### Search Product Documentation with VS
# MAGIC Next, we will create a search tool (written in SQL) that will search _unstructured_ product documentation. Note that this is based on [cosine similarity search](https://en.wikipedia.org/wiki/Cosine_similarity).
# MAGIC
# MAGIC This tool searches through product documentation to help with technical support and troubleshooting. When customers have issues with specific products, agents can use this tool to quickly find relevant documentation, setup instructions, or troubleshooting guides.
# MAGIC
# MAGIC **This function uses the vector search endpoint we created in the Setting up the Workspace notebook.**

# COMMAND ----------

spark.sql(f"""
-- Create a function to search product documentation using vector search
CREATE OR REPLACE FUNCTION {catalog_name}.{schema_name}.search_product_docs(
  search_term STRING COMMENT 'Search term for finding relevant product documentation'
)
RETURNS TABLE
COMMENT 'Searches product documentation using vector search to retrieve relevant documentation excerpts for troubleshooting and support. This should be used to search by product as each product has its own documentation.'
RETURN(
  SELECT
    product_name,
    indexed_doc as doc
  FROM
    vector_search(
      index => '{catalog_name}.{schema_name}.product_docs_index',
      query_vector => ai_query("databricks-gte-large-en",search_term,"STRING"
),
      num_results => 1
  )
);
""")

# COMMAND ----------

# MAGIC %md
# MAGIC To test the function, let's search by product. Note that we don't need to provide the exact product name, as vector search will be based on similarity search.

# COMMAND ----------

spark.sql(f"""
-- Test the search_product_docs function
SELECT product_name 
FROM {catalog_name}.{schema_name}.search_product_docs('stream master');
""").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Enabling Tooling in AI Playground
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
# MAGIC     - Repeat for `get_latest_return`, `get_service_history`, and `get_return_policy`
# MAGIC
# MAGIC 1. **Test the Functions**
# MAGIC    - In the chat window, type a prompt that would require the agent to use one or more of your tools.  
# MAGIC      Example prompts:
# MAGIC      - “Show me the latest customer return.”
# MAGIC      - “I would like information on the stream master.”
# MAGIC
# MAGIC 5. **Review the Output**
# MAGIC    - Check the agent’s response and verify that the output matches the expected results from your functions.
# MAGIC
# MAGIC 6. **Compare Model Responses (Optional)**
# MAGIC    - You can add multiple endpoints or models to compare how different LLMs use your tools. However, please note that Databricks Free Edition places caps on the number of queries to some models.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> |
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> |
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>