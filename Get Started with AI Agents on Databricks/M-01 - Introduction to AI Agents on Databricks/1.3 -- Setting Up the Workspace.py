# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Setting Up the Workspace
# MAGIC
# MAGIC This notebook will setup and discuss the Unity Catalog (UC) assets needed for successful completion of the course.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Important: Select Environment 4
# MAGIC The cells below may not work in other environments. To choose environment 4: 
# MAGIC 1. Click the ![environment.png](../../Includes/images/environment.png "environment.png") button on the right sidebar
# MAGIC 1. Open the **Environment version** dropdown
# MAGIC 1. Select **4**

# COMMAND ----------

# MAGIC %md
# MAGIC ## REQUIRED - Classroom Setup
# MAGIC This notebook will guide you through setting up your workspace for the rest of the course.
# MAGIC
# MAGIC Start by running the following cell. This will create a:
# MAGIC - catalog called "dbacademy"
# MAGIC - schema within **dbacademy** called "get_started_agents"
# MAGIC - volume within **get_started_agents** called "customer_service"

# COMMAND ----------

####################################################################################
# Set python variables for catalog, schema, and volume names (change, if desired)
catalog_name = "dbacademy"
schema_name = "get_started_agents"
volume_name = "customer_service"
####################################################################################

####################################################################################
# Create the catalog, schema, and volume if they don't exist already
spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog_name}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog_name}.{schema_name}.{volume_name}")
####################################################################################


# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup Data Files
# MAGIC In the materials for this course, there are data files for four tables. One of these tables will be used as a vector index. Follow the steps below to download the data files. You will then upload the files to the **customer_service**  volume.
# MAGIC 1. Open the workspace pane by clicking the folder icon just to the right of the left navigation bar.
# MAGIC 2. Click the left facing arrow to get to the parent folder.
# MAGIC 3. Mouseover the **Data Files** directory, and click the three-dot (kebab) menu to the right of the folder name.
# MAGIC 4. Mouseover **Download as** and click **Zip - Source (notebooks + files only)**.
# MAGIC 5. Unzip the folder on your local machine.
# MAGIC
# MAGIC Now that we have downloaded the files from the course materials, we need to upload the files to **customer_service**, created by the previous code cell:
# MAGIC
# MAGIC 1. Right-click **Catalog** in the left navigation bar, and select "Open Link in New Tab".
# MAGIC 2. On that tab, open the **dbacademy** catalog and the **get_started_agents** schema.
# MAGIC 3. Click on the **customer_service** volume.
# MAGIC 4. In the upper-right corner, click **Upload to this volume**
# MAGIC
# MAGIC Inside the folder you unzipped above, there is a folder called "Data Files". Note that there may be two folders called "Data Files". In the steps below, you want the one that contains the files/folder:
# MAGIC
# MAGIC - cust_service_data.csv
# MAGIC - policies.csv
# MAGIC - product_docs_indexed
# MAGIC - product_docs.csv
# MAGIC
# MAGIC 5. Drag this folder from your local machine to the drop zone, and click **Upload**.
# MAGIC
# MAGIC After the files upload to the volume, click the "Data Files" folder in the volume and verify that it contains the files listed above. Then, run the following cell.

# COMMAND ----------

####################################################################################
# Create tables from the data files uploaded in the previous step
def create_table(file_name):
    volume_file_path = f"/Volumes/{catalog_name}/{schema_name}/{volume_name}/Data Files/{file_name}.csv"
    table_name = f"{catalog_name}.{schema_name}.{file_name}"

    df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("multiLine", "true") \
    .option("escape", '"') \
    .load(volume_file_path) \
    .write.mode("overwrite").format("delta").saveAsTable(table_name)
create_table("cust_service_data")
create_table("policies")
create_table("product_docs")
####################################################################################

####################################################################################
# Create Delta table that will be our vector index
volume_file_path = f"/Volumes/{catalog_name}/{schema_name}/{volume_name}/Data Files/product_docs_indexed/"
table_name = f"{catalog_name}.{schema_name}.product_docs_indexed"

df = spark.read.format("delta") \
.load(volume_file_path) \
.write.mode("overwrite").format("delta").saveAsTable(table_name)
####################################################################################

####################################################################################
# Enable Change Data Feed for the "product_docs_indexed" table, so we can create a vector search index on it
spark.sql(f"ALTER TABLE {catalog_name}.{schema_name}.product_docs_indexed SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
####################################################################################


####################################################################################
# Create two functions we will use later in the course
spark.sql(f"""
-- Create a function to get service history by user
CREATE OR REPLACE FUNCTION {catalog_name}.{schema_name}.get_service_history(
    user_email STRING COMMENT 'User email to retrieve order history'
    )
    RETURNS TABLE (
    returns_last_12_months INT,
    issue_category STRING, 
    todays_date DATE
    )
    COMMENT 'This takes the user_name of a customer as an input and returns the number of returns and the issue category'
    LANGUAGE SQL
    RETURN(
    SELECT count(*) as returns_last_12_months, issue_category, now() as todays_date
    FROM {catalog_name}.{schema_name}.cust_service_data 
    WHERE email = user_email
    GROUP BY issue_category
    );""")
spark.sql(f"""
-- Create a function to retrieve company policy details
CREATE OR REPLACE FUNCTION {catalog_name}.{schema_name}.get_return_policy(
    policy_name STRING COMMENT 'Policy name to return. Example policies: Account Cancellation Policy, Exchange Policy, Refund Policy, Warranty Policy, Privacy Policy, Return Policy'
    )
    RETURNS TABLE (
    policy           STRING,
    policy_details   STRING,
    last_updated     DATE
    )
    COMMENT 'Returns the details of the Return Policy'
    LANGUAGE SQL
    RETURN (
    SELECT
    policy,
    policy_details,
    last_updated
    FROM {catalog_name}.{schema_name}.policies
    WHERE policy = policy_name
    LIMIT 1
    );
    """)
####################################################################################

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Vector Index
# MAGIC In order to test the agent we will be creating, we need to setup a vector search index. To do this, complete the following:
# MAGIC
# MAGIC 1. First, create a vector search endpoint called "vs_endpoint_1" by completing the following:
# MAGIC
# MAGIC - Right-click **Compute** in the left navigation bar and select "Open Link in New Tab"
# MAGIC - Click **Vector Search** in the top tab list
# MAGIC - Click **Create endpoint** on the right side
# MAGIC - Name the endpoint "vs_endpoint_1"
# MAGIC - Click **Confirm**.
# MAGIC
# MAGIC 2. Create index on the endpoint
# MAGIC - Click **Create index** in the center of the screen
# MAGIC - Select **dbacademy.get_started_agents.product_docs_indexed** and click **Next**
# MAGIC - Name the index "product_docs_index"
# MAGIC - Select "product_id" for the **Primary key**
# MAGIC - Leave **Column to sync** blank, so we index all columns
# MAGIC - Under **Embeddings**, select "Use existing embedding column"
# MAGIC - For **Embedding vector column** select "__db_indexed_doc_vector"
# MAGIC - For **Embedding dimension**, type "1024"
# MAGIC - For **Vector search endpoint**, select "vs_endpoint_1"
# MAGIC - Ensure **Triggered** is selected
# MAGIC - Click **Create**
# MAGIC
# MAGIC **Note:** The initial setup and sync will take 5-10 minutes. You can continue with the course while the index is getting set up.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Explore The Datasets
# MAGIC
# MAGIC Let's examine the customer service datasets that were created during our setup. In total, three were brought in and stored as Delta tables inside Unity Catalog:
# MAGIC 1. `cust_service_data`
# MAGIC 1. `policies`
# MAGIC 1. `product_docs`
# MAGIC 1. `product_docs_index`
# MAGIC     - This is a pre-built vector search index. The topic of embeddings falls outside this course, but essentially, embeddings are generated by a large language model and are a key component of many generative AI applications that depend on finding documents or images that are similar to each other. You can explore more on this topic [here](https://docs.databricks.com/aws/en/generative-ai/vector-search#what-is-mosaic-ai-vector-search).
# MAGIC     
# MAGIC Let's explore the data.

# COMMAND ----------

# MAGIC %md
# MAGIC ### A1. Data Exploration with the UI
# MAGIC
# MAGIC #### Instructions
# MAGIC 1. Right-click on **Catalog** in the navigation menu and select, **Open Link in New Tab**. 
# MAGIC 1. In the **dbacademy** catalog click on the **get_started_agents** schema. 
# MAGIC 1. Click on tables and you will see the tables **cust_service_data**, **policies**, and **product_docs**, in addition to the vector search index tables, called **product_docs_index** and **product_docs_indexed**. 
# MAGIC 1. Click on **Volumes** inside the **get_started_agents** schema, and you will see the volume **customer_service**. Here you will find CSV files that were used to create the tables. Note that it is best practice to store all data file types in a volume within Unity Catalog.

# COMMAND ----------

# MAGIC %md
# MAGIC ### A2. Data Exploration with SQL
# MAGIC
# MAGIC We can use this notebook to read in these datasets and explore them here as well. For example, run the next cell to view one of the Delta tables we created as a part of the setup script called `cust_service_data`.
# MAGIC
# MAGIC **Note**: We are using a call to `spark.sql` to make working with variables easier. This cell could have used SQL if we weren't using any variables.

# COMMAND ----------

spark.sql(f"SELECT * FROM {catalog_name}.{schema_name}.cust_service_data;").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. SQL Functions
# MAGIC Next, let's view some SQL functions that were created as a part of the setup for this workspace. SQL functions are a key ingredient for agentic use cases for both structured and unstructured data.
# MAGIC > ### What Are SQL Functions?
# MAGIC > [SQL functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-sql-function) are named blocks of logic that perform operations on data within a database. These functions allow you to encapsulate computations, transformations, or queries so they can be reused, improving code clarity and maintainability.

# COMMAND ----------

# MAGIC %md
# MAGIC ### B1. Locating SQL Functions in UC
# MAGIC As a part of the setup, we have created two SQL functions called `get_return_policy()` and `get_service_history()`. 
# MAGIC - `get_return_policy()`: A function that will access the internal knowledge base or policy documents related to returns, refunds, and exchanges. The goal of creating this tool is to verify you are in compliance with company guidelines, which prevents potential errors and conflicts.
# MAGIC - `get_service_history()`: A function that queries the order management system or customer database by the user's email. The goal of this tool is to review past purchases, return patterns, and any specific notes to help determine appropriate next steps (e.g., confirm eligibility for return).
# MAGIC #### Instructions
# MAGIC 1. Open the **dbacademy** catalog again in a separate window and click on the `get_started_agents` schema. There, you will see the two functions mentioned above. 
# MAGIC 1. Click on `get_return_policy`. Here you will see
# MAGIC     - The description of the SQL function. 
# MAGIC     - The **Definition** (the query)
# MAGIC     - The function's metadata (**type**, **Return type**, etc.)
# MAGIC     - The **Details**, which shows things like who created it and the security type.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. A Vector Search Endpoint
# MAGIC As a part of the setup, we provisioned a standard vector search endpoint. Databricks' Vector Search is a robust product designed for storing and retrieving embeddings, which are mathematical representations of the semantic content of data, including text and images. This functionality integrates seamlessly into the Lakehouse architecture, enabling users to execute queries that return the most semantically similar data based on the input vector.
# MAGIC
# MAGIC ### Instructions
# MAGIC 1. To see the vector search endpoint that was created, navigate to **Compute** on the left side menu and select **Vector Search**. There you will see a status of **Ready** next to the endpoint with the name **vs_endpoint_1**. Note that this might say **provisioning**, depending on when you are viewing this during the setup.  
# MAGIC > ### What is Vector Search on Databricks?
# MAGIC > Databricks' Vector Search is a robust product designed for storing and retrieving embeddings, which are mathematical representations of the semantic content of data, including text and images. This functionality integrates seamlessly into the Lakehouse architecture, enabling users to execute queries that return the most semantically similar data based on the input vector. You can read more [here](https://www.databricks.com/product/machine-learning/vector-search). 
# MAGIC
# MAGIC _This course does not go into detail on deploying a vector search endpoint. Please see our [other](https://www.databricks.com/training/catalog?search=generative+ai+solution+development) course offerings on this topic._

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC After working through this demonstration, you now have a better understanding of the different assets that we created as a part of your workspace, such as UC Assets and a Databricks Vector Search Endpoint.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> |
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> |
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>