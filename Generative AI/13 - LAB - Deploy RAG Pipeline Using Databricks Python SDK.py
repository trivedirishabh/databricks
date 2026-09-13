# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # LAB - End-to-end RAG Pipeline
# MAGIC
# MAGIC In this lab, you will build a Retrieval-Augmented Generation (RAG) pipeline on Databricks using various generative AI tools.
# MAGIC
# MAGIC **Lab Outline:**
# MAGIC
# MAGIC - **Task 1**: Create a vector search index.
# MAGIC - **Task 2**: Build the RAG model.
# MAGIC - **Task 3**: Register the RAG model.
# MAGIC - **Task 4**: Deploy the model.
# MAGIC
# MAGIC **📌 Your Task: In this lab, your task is to replace `<FILL_IN>` sections with appropriate code.**
# MAGIC
# MAGIC >Please note: This notebook is nearly identical to the [00 - REQUIRED Initial Setup]($./00 - REQUIRED Initial Setup) notebook. You can use that notebook as a reference to help you with the `<FILL_IN>` code.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC >IMPORTANT: In this lesson, you will create a vector search endpoint, a vector search index, a RAG application, and finish by deploying the application to an endpoint. Some of these processes take 10-20 minutes. Also, Databricks Free Edition places caps on the number of vector search endpoints and model serving endpoints you can have configured. If you run into errors, double-check that you are not exceeding these caps.

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

# COMMAND ----------

# MAGIC %pip install databricks-vectorsearch databricks-langchain langchain==0.3.27 databricks-agents 
# MAGIC
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Classroom Setup
# MAGIC The following cell:
# MAGIC 1. Captures your username and creates an endpoint name based on that username
# MAGIC 1. Creates the **dbacademy** catalog and **get_started_genai** schema if they do not already exist.

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
spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog_name}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}")
####################################################################################

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create a Table with Sample Data
# MAGIC Code in the following cell uses the `%run` magic command to run another notebook in the same directory as this one. The notebook is called [create_e_commerce_sample_dataset]($./create_e_commerce_sample_dataset). This notebook creates a table in the `dbacademy` catalog and `get_started_genai` schema called `e_commerce_product_listings_dataset`.
# MAGIC
# MAGIC After running the following cell, you can find the `e_commerce_product_listings_dataset` in the Catalog Explorer.

# COMMAND ----------

# MAGIC %run ./create_e_commerce_sample_dataset

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create a Table for the Vector Search Index
# MAGIC The following cell creates a table we will use for our vector search index and enables change data feed.

# COMMAND ----------

dataset = spark.sql(f"""
    SELECT 
        ASIN AS id,
        CONCAT(
            '## Title: ', Title, '\n\n',
            '## Description: ', Description, '\n\n',
            '## URL: ', URL
        ) AS document
    FROM {catalog_name}.{schema_name}.e_commerce_product_listings_dataset
""")

# Create a delta table for the dataset
vs_source_table_name = f"{catalog_name}.{schema_name}.product_text"
dataset.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(<FILL_IN>)

# Enable Change Data Feed
spark.sql(f"ALTER TABLE {vs_source_table_name} SET TBLPROPERTIES (delta.<FILL_IN> = true)")

# COMMAND ----------

# MAGIC %skip 
# MAGIC dataset = spark.sql(f"""
# MAGIC     SELECT 
# MAGIC         ASIN AS id,
# MAGIC         CONCAT(
# MAGIC             '## Title: ', Title, '\n\n',
# MAGIC             '## Description: ', Description, '\n\n',
# MAGIC             '## URL: ', URL
# MAGIC         ) AS document
# MAGIC     FROM {catalog_name}.{schema_name}.e_commerce_product_listings_dataset
# MAGIC """)
# MAGIC
# MAGIC # Create a delta table for the dataset
# MAGIC vs_source_table_name = f"{catalog_name}.{schema_name}.product_text"
# MAGIC dataset.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(vs_source_table_name)
# MAGIC
# MAGIC spark.sql(f"ALTER TABLE {vs_source_table_name} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Vector Search Index
# MAGIC This code creates a vector search endpoint and a vector search index on that endpoint. Although the code takes very little time to run, the index will not be ready for about 20 minutes.
# MAGIC
# MAGIC >Note: If you are using Databricks Free Edition and you get an error that says that your quota has been exceeded, you will not be able to successfully run this cell until you delete the existing vector search endpoint. To do this:
# MAGIC
# MAGIC - Click **Compute** in the left navigation.
# MAGIC
# MAGIC - Click the **Vector Search** tab.
# MAGIC
# MAGIC - Mouseover the name of the endpoint. On the right side, click the three-dot (kebab) menu, and select "Delete endpoint".

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()

vs_endpoint_name = "vector_search_endpoint"
vs_index_table_name = f"{catalog_name}.{schema_name}.product_embeddings"

vsc.create_endpoint(
    name=vs_endpoint_name,
    endpoint_type="STANDARD"
)

vsc.create_delta_sync_index(
    endpoint_name="vector_search_endpoint",
    index_name=vs_index_table_name,
    source_table_name=f"{catalog_name}.{schema_name}.product_text",
    pipeline_type="TRIGGERED", 
    primary_key="id",            # Unique identifier column in source table
    embedding_source_column="document",
    embedding_model_endpoint_name="databricks-gte-large-en" # Serving endpoint
)


# COMMAND ----------

# MAGIC %md
# MAGIC ### Check if VS Index is Ready
# MAGIC Run the following cell to check if the index is ready. The index will take approximately 20 minutes to be ready.

# COMMAND ----------

import time

def wait_for_index_to_be_ready(vsc, vs_endpoint_name, index_name):
  for i in range(180):
    idx = vsc.get_index(vs_endpoint_name, index_name).describe()
    index_status = idx.get('status', idx.get('index_status', {}))
    status = index_status.get('detailed_state', index_status.get('status', 'UNKNOWN')).upper()
    url = index_status.get('index_url', index_status.get('url', 'UNKNOWN'))
    if "ONLINE" in status:
      print("Index is ready!!")
      return
    if "UNKNOWN" in status:
      print(f"Can't get the status - will assume index is ready {idx} - url: {url}")
      return
    elif "PROVISIONING" in status:
      if i % 20 == 0: print(f"\nWaiting for index to be ready. This takes about 20 minutes.\n{index_status} - pipeline url:{url}")
      time.sleep(10)
    else:
        raise Exception(f'''Error with the index - this shouldn't happen. Pipeline might have been killed.\n Please delete it and re-run the previous cell: vsc.delete_index("{index_name}, {vs_endpoint_name}") \nIndex details: {idx}''')
  raise Exception(f"Timeout, your index isn't ready yet: {vsc.get_index(index_name, vs_endpoint_name)}")

wait_for_index_to_be_ready(vsc, vs_endpoint_name, vs_index_table_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ###  Testing the Index: Search for Products Similar to the Query
# MAGIC
# MAGIC Before building the RAG pipeline, let's check if the index is ready. We will use the `similarity_search` function to search for products that are similar to the query text.

# COMMAND ----------

vs_endpoint_name = "vector_search_endpoint"
vs_index_table_name = f"{catalog_name}.{schema_name}.product_embeddings"

from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient(disable_notice=True)

question = "handmade lamp with remote control"

try:
    # get index created in the previous step
    index = vsc.get_index(vs_endpoint_name, vs_index_table_name)

    # search for similar documents
    results = index.<FILL_IN>(
        query_text = question,
        columns=["document"],
        num_results=4
    )

    # show the results
    docs = results.get("result", {}).get("data_array", [])
    print("\n")
    for doc in docs:
        print(doc[0])

except Exception as e:
    print(f"Error occurred while loading the index. Did you accidentally delete the index created in the 00 - REQUIRED Initial Setup notebook?: {e}")

# COMMAND ----------

# MAGIC %skip
# MAGIC vs_endpoint_name = "vector_search_endpoint"
# MAGIC vs_index_table_name = f"{catalog_name}.{schema_name}.product_embeddings"
# MAGIC
# MAGIC from databricks.vector_search.client import VectorSearchClient
# MAGIC
# MAGIC vsc = VectorSearchClient(disable_notice=True)
# MAGIC
# MAGIC question = "handmade lamp with remote control"
# MAGIC
# MAGIC try:
# MAGIC     # get index created in the previous step
# MAGIC     index = vsc.get_index(vs_endpoint_name, vs_index_table_name)
# MAGIC
# MAGIC     # search for similar documents
# MAGIC     results = index.similarity_search(
# MAGIC         query_text = question,
# MAGIC         columns=["document"],
# MAGIC         num_results=4
# MAGIC     )
# MAGIC
# MAGIC     # show the results
# MAGIC     docs = results.get("result", {}).get("data_array", [])
# MAGIC     print("\n")
# MAGIC     for doc in docs:
# MAGIC         print(doc[0])
# MAGIC
# MAGIC except Exception as e:
# MAGIC     print(f"Error occurred while loading the index. Did you accidentally delete the index created in the 00 - REQUIRED Initial Setup notebook?: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Build a RAG Model
# MAGIC With our contextual information prepared and indexed in Vector Search, we can proceed to build a RAG chain.
# MAGIC

# COMMAND ----------

import mlflow
from operator import itemgetter
from databricks.vector_search.client import VectorSearchClient
from databricks_langchain import ChatDatabricks, DatabricksVectorSearch, DatabricksEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

mlflow.langchain.autolog()

# define a retriever function that will be used in the chain
def vector_search_as_retriever(persist_dir=None):
    vectorstore = DatabricksVectorSearch(f"{catalog_name}.{schema_name}.product_embeddings")
    return vectorstore.as_retriever(search_kwargs={"k": 3})

# Return the string contents of the most recent messages: [{...}] from the user to be used as input question
def extract_user_query_string(chat_messages_array):
    return chat_messages_array[-1]["content"]

def format_context(docs):
    chunk_contents = [f"Passage: {d.page_content}\n" for d in docs]
    return "".join(chunk_contents)

# define template for prompt
prompt_template = PromptTemplate.from_template(
    """
    You are a hand-crafted product design expert and your task is to creative products that are very good and can be sold online.

    Write a product title and description that is similar to the following product title and item details.

    Maximum 300 words.

    Use the following product title and details as example;

    <context>
    {context}
    </context>

    Question: {question}

    Answer:
    """
)

# define foundation model for generating responses
model = ChatDatabricks(endpoint="databricks-meta-llama-3-3-70b-instruct", max_tokens = 500, temperature=0.8)

# RAG chain
chain = (
    {
        "question": itemgetter("messages") | RunnableLambda(extract_user_query_string),
        "context": itemgetter("messages")
        | RunnableLambda(extract_user_query_string)
        | vector_search_as_retriever
        | RunnableLambda(format_context),
    }
    | prompt_template
    | model
    | StrOutputParser()
)

# let's give it a try:
input_example = {"messages": [ {"role": "user", "content": "handmade lamp with remote control"}]}
answer = chain.<FILL_IN>(input_example)
print(answer)

# COMMAND ----------

# MAGIC %skip
# MAGIC import mlflow
# MAGIC from operator import itemgetter
# MAGIC from databricks.vector_search.client import VectorSearchClient
# MAGIC from databricks_langchain import ChatDatabricks, DatabricksVectorSearch, DatabricksEmbeddings
# MAGIC from langchain.chains import create_retrieval_chain
# MAGIC from langchain.chains.combine_documents import create_stuff_documents_chain
# MAGIC from langchain.prompts import (
# MAGIC     PromptTemplate,
# MAGIC     ChatPromptTemplate,
# MAGIC )
# MAGIC from langchain_core.runnables import RunnableLambda
# MAGIC from langchain_core.runnables import RunnablePassthrough
# MAGIC from langchain_core.output_parsers import StrOutputParser
# MAGIC
# MAGIC mlflow.langchain.autolog()
# MAGIC
# MAGIC # define a retriever function that will be used in the chain
# MAGIC def vector_search_as_retriever(persist_dir=None):
# MAGIC     vectorstore = DatabricksVectorSearch(f"{catalog_name}.{schema_name}.product_embeddings")
# MAGIC     return vectorstore.as_retriever(search_kwargs={"k": 3})
# MAGIC
# MAGIC # Return the string contents of the most recent messages: [{...}] from the user to be used as input question
# MAGIC def extract_user_query_string(chat_messages_array):
# MAGIC     return chat_messages_array[-1]["content"]
# MAGIC
# MAGIC def format_context(docs):
# MAGIC     chunk_contents = [f"Passage: {d.page_content}\n" for d in docs]
# MAGIC     return "".join(chunk_contents)
# MAGIC
# MAGIC # define template for prompt
# MAGIC prompt_template = PromptTemplate.from_template(
# MAGIC     """
# MAGIC     You are a hand-crafted product design expert and your task is to creative products that are very good and can be sold online.
# MAGIC
# MAGIC     Write a product title and description that is similar to the following product title and item details.
# MAGIC
# MAGIC     Maximum 300 words.
# MAGIC
# MAGIC     Use the following product title and details as example;
# MAGIC
# MAGIC     <context>
# MAGIC     {context}
# MAGIC     </context>
# MAGIC
# MAGIC     Question: {question}
# MAGIC
# MAGIC     Answer:
# MAGIC     """
# MAGIC )
# MAGIC
# MAGIC # define foundation model for generating responses
# MAGIC model = ChatDatabricks(endpoint="databricks-meta-llama-3-3-70b-instruct", max_tokens = 500, temperature=0.8)
# MAGIC
# MAGIC # RAG chain
# MAGIC chain = (
# MAGIC     {
# MAGIC         "question": itemgetter("messages") | RunnableLambda(extract_user_query_string),
# MAGIC         "context": itemgetter("messages")
# MAGIC         | RunnableLambda(extract_user_query_string)
# MAGIC         | vector_search_as_retriever
# MAGIC         | RunnableLambda(format_context),
# MAGIC     }
# MAGIC     | prompt_template
# MAGIC     | model
# MAGIC     | StrOutputParser()
# MAGIC )
# MAGIC
# MAGIC # let's give it a try:
# MAGIC input_example = {"messages": [ {"role": "user", "content": "handmade lamp with remote control"}]}
# MAGIC answer = chain.invoke(input_example)
# MAGIC print(answer)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Save the Model to Model Registry in Unity Catalog
# MAGIC Now that our chain is ready, we can register it within our Unity Catalog schema. 

# COMMAND ----------

import mlflow
import langchain
import langchain_community
import databricks.vector_search
from mlflow.models import infer_signature
from mlflow.models.resources import (
    DatabricksVectorSearchIndex
)

# Set Model Registry URI to Unity Catalog
mlflow.<FILL_IN>("databricks-uc")

model_name = f"{catalog_name}.{schema_name}.getstarted_genai_rag_demo"
input_example = {"messages": [ {"role": "user", "content": "handmade lamp with remote control"}]}

# Register the assembled RAG model in Model Registry with Unity Catalog
with mlflow.<FILL_IN>(run_name="genai_gs_demo_02_01") as run:
    signature = infer_signature(input_example, answer)
    model_info = mlflow.langchain.log_model(
        lc_model=chain,
        artifact_path="chain",
        input_example=input_example,
        signature=signature,
        pip_requirements=[
            "langchain==" + langchain.__version__,
            "langchain-community==" + langchain_community.__version__,
            "databricks-vectorsearch==" + databricks.vector_search.__version__,
            "databricks_langchain"
        ],
        resources=[
            DatabricksVectorSearchIndex(index_name=f"{catalog_name}.{schema_name}.product_embeddings")
        ]
    )

mlflow.register_model(model_info.model_uri, model_name)

# COMMAND ----------

# MAGIC %skip
# MAGIC import mlflow
# MAGIC import langchain
# MAGIC import langchain_community
# MAGIC import databricks.vector_search
# MAGIC from mlflow.models import infer_signature
# MAGIC from mlflow.models.resources import (
# MAGIC     DatabricksVectorSearchIndex
# MAGIC )
# MAGIC
# MAGIC # Set Model Registry URI to Unity Catalog
# MAGIC mlflow.set_registry_uri("databricks-uc")
# MAGIC
# MAGIC model_name = f"{catalog_name}.{schema_name}.getstarted_genai_rag_demo"
# MAGIC input_example = {"messages": [ {"role": "user", "content": "handmade lamp with remote control"}]}
# MAGIC
# MAGIC # Register the assembled RAG model in Model Registry with Unity Catalog
# MAGIC with mlflow.start_run(run_name="genai_gs_demo_02_01") as run:
# MAGIC     signature = infer_signature(input_example, answer)
# MAGIC     model_info = mlflow.langchain.log_model(
# MAGIC         lc_model=chain,
# MAGIC         artifact_path="chain",
# MAGIC         input_example=input_example,
# MAGIC         signature=signature,
# MAGIC         pip_requirements=[
# MAGIC             "langchain==" + langchain.__version__,
# MAGIC             "langchain-community==" + langchain_community.__version__,
# MAGIC             "databricks-vectorsearch==" + databricks.vector_search.__version__,
# MAGIC             "databricks_langchain"
# MAGIC         ],
# MAGIC         resources=[
# MAGIC             DatabricksVectorSearchIndex(index_name=f"{catalog_name}.{schema_name}.product_embeddings")
# MAGIC         ]
# MAGIC     )
# MAGIC
# MAGIC mlflow.register_model(model_info.model_uri, model_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Serve the Model on Mosaic AI Model Serving
# MAGIC With the model registered, we can deploy it to a serving endpoint. This process will take about 10-15 minutes.
# MAGIC
# MAGIC >Note: If you are using Databricks Free Edition and you get an error in the cell below that you have exceeded your quota, you will not be able to succussfully run the cell. To delete an existing endpoint:
# MAGIC
# MAGIC - Click **Serving** in the left navigation.
# MAGIC
# MAGIC - Click the name of the serving endpoint.
# MAGIC
# MAGIC - Click the three-dot (kebab) menu in the upper-right corner, and select "Delete".

# COMMAND ----------

from mlflow.deployments import get_deploy_client

client = get_deploy_client("databricks")
model_name = f"{catalog_name}.{schema_name}.getstarted_genai_rag_demo"

# Check if the endpoint already exists
try:
    # Attempt to get the endpoint
    existing_endpoint = client.get_endpoint(endpoint_name)
    print(f"Endpoint '{endpoint_name}' already exists.")
except Exception as e:
    # If not found, create the endpoint
    if "RESOURCE_DOES_NOT_EXIST" in str(e):
        print(f"Creating a new endpoint: {endpoint_name}")
        endpoint = client.create_endpoint(
            name=endpoint_name,
            config={
                "served_entities": [
                    {
                        "name": "my-model",
                        "entity_name": model_name,
                        "entity_version": 1,
                        "workload_size": "Small",
                        "scale_to_zero_enabled": True
                    }
                ],
                "traffic_config": {
                    "routes": [
                        {
                            "served_model_name": "my-model",
                            "traffic_percentage": 100
                        }
                    ]
                }
            }
        )
    else:
        print(f"An error occurred: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>