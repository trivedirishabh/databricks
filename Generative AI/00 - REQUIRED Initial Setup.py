# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Welcome to the Course!!
# MAGIC Welcome to Get Started with Databricks for Generative AI!! This course is designed for data enthusiasts, analysts, and aspiring AI engineers who want to move beyond simple chatbots and understand how to develop enterprise-grade AI applications. You will begin by exploring the core principles of generative AI before diving into the Databricks Data Intelligence Platform. No prior experience with AI modeling is required; we start with the fundamentals to ensure you have a solid foundation in how machines learn to generate human-like text, code, and insights.
# MAGIC
# MAGIC ## Master the Mosaic AI Ecosystem
# MAGIC You will get hands-on experience with Mosaic AI, the powerhouse suite within Databricks that simplifies the entire AI lifecycle. We will guide you through building a Retrieval-Augmented Generation (RAG) pipeline, which allows your AI to "read" and answer questions based on your own private data safely and accurately. You’ll learn to use Vector Search for organizing information, MLflow for tracking your experiments, and Unity Catalog to ensure your models are secure and governed. By the end of this course, you won't just know what generative AI is—-you’ll have the practical skills to deploy, evaluate, and monitor your own AI agents in a professional production environment.
# MAGIC
# MAGIC >Please note: This course will run in Databricks Free Edition. However, please note that we will be deploying a vector search index, which requires a vector search endpoint, and we will be deploying a finished model to Mosaic AI Model Serving. Databricks Free Edition has caps on the number of vector search endpoints and model serving endpoints you can deploy. If you run into errors deploying this infrastructure, please double-check that you have not hit these caps.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Initial Setup
# MAGIC We need to configure the environment in order to complete the lessons in the course. In this notebook, we will do the following:
# MAGIC
# MAGIC 1. Setup the serverless environment.
# MAGIC 1. Create a catalog and schema.
# MAGIC 1. Create a table that contains some sample e-commerce data. We will use this table in our vector search index later in the course.
# MAGIC 1. Deploy a RAG model to a Mosaic AI model serving endpoint.
# MAGIC
# MAGIC >Please note: The lessons in this course will show you how to create a vector search endpoint, a vector search index, a RAG application, and finish by deploying the application to an endpoint. Some of these processes take 10-20 minutes. In order to save time, we are using the Databricks SDK to create the infrastructure before we actually discuss how it works. More detailed information about these topics follows in the lessons.

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
# MAGIC 1. Creates a catalog called **dbacademy** and a schema called **get_started_genai**.

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
dataset.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(vs_source_table_name)

spark.sql(f"ALTER TABLE {vs_source_table_name} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Vector Search Index
# MAGIC This code creates a vector search endpoint and a vector search index on that endpoint. Although the code takes very little time to run, the index will not be ready for about 20 minutes.
# MAGIC
# MAGIC >Reminder: We will discuss how to create a vector search index in the following lessons.

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()

vsc.create_endpoint(
    name="vector_search_endpoint",
    endpoint_type="STANDARD"
)

vsc.create_delta_sync_index(
    endpoint_name="vector_search_endpoint",
    index_name=f"{catalog_name}.{schema_name}.product_embeddings",
    source_table_name=f"{catalog_name}.{schema_name}.product_text",
    pipeline_type="TRIGGERED", 
    primary_key="id",            # Unique identifier column in source table
    embedding_source_column="document",
    embedding_model_endpoint_name="databricks-gte-large-en" # Serving endpoint
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## Build a RAG Model
# MAGIC With our contextual information prepared and indexed in Vector Search, we can proceed to build a RAG chain.
# MAGIC
# MAGIC >Reminder: We will discuss how to create a RAG application in the following lessons.

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

# COMMAND ----------

# MAGIC %md
# MAGIC ## Save the Model to Model Registry in Unity Catalog
# MAGIC Now that our chain is ready, we can register it within our Unity Catalog schema. 
# MAGIC > Reminder: We will explain how to do this in the lessons that follow.

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
mlflow.set_registry_uri("databricks-uc")

model_name = f"{catalog_name}.{schema_name}.getstarted_genai_rag_demo"
input_example = {"messages": [ {"role": "user", "content": "handmade lamp with remote control"}]}

# Register the assembled RAG model in Model Registry with Unity Catalog
with mlflow.start_run(run_name="genai_gs_demo_02_01") as run:
    signature = infer_signature(input_example, "answer")
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

# MAGIC %md
# MAGIC ### Serve the Model on Mosaic AI Model Serving
# MAGIC With the model registered, we can deploy it to a serving endpoint. This process will take about 10-15 minutes.
# MAGIC >Reminder: We will be discussing how to do this in a future lesson.

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