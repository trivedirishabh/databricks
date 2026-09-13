# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Building and Registering a RAG Model
# MAGIC
# MAGIC A Retrieval-Augmented Generation (RAG) model is a widely used architecture for generative AI applications, particularly when contextual information needs to accompany the prompt. **In this demo, we will construct a RAG pipeline and register it in the Unity Catalog model registry.**
# MAGIC
# MAGIC The RAG pipeline will function as a simple **product design chatbot**. As contextual information, we will provide product descriptions that have previously **listed on Etsy website**. Please note that the dataset **we will use is publicly available, and the large language model (LLM) might already include this data in its training set**. Consequently, the quality of responses with and without contextual data might not differ significantly. In a real-world scenario, the contextual data would include information that is new to the LLM.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC By the end of this demo, you will be able to:
# MAGIC
# MAGIC - Inspect the Vector Search endpoint and index using the UI.
# MAGIC
# MAGIC - Set up a Vector Search index using an existing Delta table.
# MAGIC
# MAGIC - Retrieve documents from the vector store using similarity search.
# MAGIC
# MAGIC - Assemble a RAG pipeline by integrating various components.
# MAGIC
# MAGIC - Register a RAG pipeline in the Model Registry.

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

# MAGIC %pip install -qq -U databricks-sdk databricks-langchain databricks-vectorsearch langsmith>=0.1.125 langchain==0.3.27 langchain-community==0.3.27 mlflow>=3.0 databricks-feature-engineering 
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

import pkg_resources
print(pkg_resources.get_distribution("langsmith").version)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Demo Overview
# MAGIC
# MAGIC The initial component of this demonstration is the **retrieval component**. Based on the input query, we will search for and retrieve similar product descriptions.
# MAGIC
# MAGIC Next, we will construct the entire pipeline using LangChain. **Please note that LangChain is not within the scope of this course. For more information, we recommend referring to the "Generative AI Engineering with Databricks" course.**
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Dataset
# MAGIC
# MAGIC Before we start building the AI chain, we will need to load a dataset. The [00 - REQUIRED Initial Setup]($./00 - REQUIRED Initial Setup) notebook created a table that contains fake e-commerce data. There are 200 rows in the table. A table that is the source for a vector search database can have a lot more rows, but our sample table will work for demonstration purposes.

# COMMAND ----------

dataset = spark.sql(f"""
    SELECT 
        *
    FROM {catalog_name}.{schema_name}.e_commerce_product_listings_dataset
""").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Delta Table as Vector Search Source
# MAGIC In the next cell, we create a table that will be used as the source table for our vector search database. We only need the product `title`, `description`, and `URL` fields, in addition to the `id`. This table will be used for creating embeddings and will be synchronized with the vector database.

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
vs_source_table_name = f"{catalog_name}.{schema_name}.product_text_example"
dataset.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(vs_source_table_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Enable Delta Change Data Feed
# MAGIC In order to keep the source table we just created and the vector search database in-sync, we need to enable Delta's Change Data Feed (CDF). More information about CDF is [here](https://docs.databricks.com/aws/en/delta/delta-change-data-feed)

# COMMAND ----------

# Enable Change Data Feed for Delta table
spark.sql(f"ALTER TABLE {vs_source_table_name} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

display(spark.sql(f"SELECT * FROM {vs_source_table_name}"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create and Test Vector Index
# MAGIC
# MAGIC In this step, we will compute embeddings for a dataset containing information about products and store them in a Vector Search index using Databricks Vector Search.
# MAGIC
# MAGIC **IMPORTANT: In the [00 - REQUIRED Initial Setup]($./00 - REQUIRED Initial Setup) notebook, a Vector Search endpoint and index was created for you. Therefore, you do not need to actually create this infrastructure. However, instructions for doing this are provided using the UI.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating a Vector Index via UI
# MAGIC
# MAGIC **Steps to Create a Vector Search Endpoint:**
# MAGIC
# MAGIC - Right-click **Compute** in the left navigation bar and select "Open Link in New Tab".
# MAGIC
# MAGIC - Click **Vector Search** in the tab bar.
# MAGIC
# MAGIC - Click **Create Endpoint**.
# MAGIC
# MAGIC - Give the endpoint a name.
# MAGIC
# MAGIC >Important: We do not need to actually click **Confirm** because an endpoint has already been created for you. If you do create an endpoint, please note that the endpoint can take up to 15 minutes to be ready.
# MAGIC
# MAGIC **Steps to Create a Vector Index:**
# MAGIC
# MAGIC Now that we have an endpoint that can host our vector search index, we can create the actual index itself. Complete the following:
# MAGIC
# MAGIC - In your other browser tab, navigate to **Catalog** from the left navigation and select the **dbacademy** catalog. 
# MAGIC
# MAGIC - Select the **get_started_genai** schema.
# MAGIC
# MAGIC - Select the **`product_text_example`** table created previously.
# MAGIC
# MAGIC - In the top right corner, click **"Create"** and then **"Vector search index"**.
# MAGIC
# MAGIC - Enter **`product_embeddings_example`** as the index name.
# MAGIC
# MAGIC - Choose `id` as the primary key.
# MAGIC
# MAGIC - Choose `document` field as column(s) to sync.
# MAGIC
# MAGIC - For embedding source, select **Compute embeddings**:
# MAGIC   - Choose `document` column as the source column.
# MAGIC   - Select **databricks-gte-large-en** as the embedding model. Embedding creation will be managed by Databricks, which means we do not need to manually compute embeddings.
# MAGIC
# MAGIC - Select a vector search endpoint to host the database.
# MAGIC
# MAGIC - Set sync mode to **"Triggered"**.
# MAGIC
# MAGIC >Important: We do not need to actually click **Create** because a vector search index has already been created for you. If you do create an index, please note that it will take up to 20 minutes to be ready.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating a Vector Index via the Databricks Python SDK 
# MAGIC
# MAGIC For simplicity, we created the vector index using the Databricks Python SDK in the [00 - REQUIRED Initial Setup]($./00 - REQUIRED Initial Setup) notebook. For more detailed instructions, please refer to the [documentation page](https://docs.databricks.com/en/generative-ai/create-query-vector-search.html#create-index-using-the-python-sdk).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Testing the Index: Search for Products Similar to the Query
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
    results = index.similarity_search(
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

# MAGIC %md
# MAGIC
# MAGIC **💡 Question:** Four similar documents are returned. What should we do if we want to **use only two of these documents** or if we want to **add documents into the context based on their importance or higher similarity**?

# COMMAND ----------

# MAGIC %md
# MAGIC ## Enable MLflow Tracing
# MAGIC
# MAGIC MLflow supports auto-logging for LangChain models. Before we begin constructing the chains, we will enable auto-logging as shown below.

# COMMAND ----------

import mlflow
mlflow.langchain.autolog()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Build a RAG Model
# MAGIC
# MAGIC With our contextual information prepared and indexed in Vector Search, we can proceed to build a RAG chain.
# MAGIC
# MAGIC With MLflow tracing enabled, you will be able to inspect the LangChain pipeline.
# MAGIC
# MAGIC **💡 Question:** Which documents are retrieved from Vector Search and used as "context"?

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

# define a retriever function that will be used in the chain
def vector_search_as_retriever(persist_dir=None):
    vectorstore = DatabricksVectorSearch(vs_index_table_name)
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
answer = chain.invoke(input_example)
print(answer)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Save the Model to Model Registry in Unity Catalog
# MAGIC
# MAGIC Now that our chain is ready and evaluated, we can register it within our Unity Catalog schema. 
# MAGIC
# MAGIC After registering the chain, you can view the chain and models in the **Catalog Explorer**.

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
            DatabricksVectorSearchIndex(index_name=vs_index_table_name)
        ]
    )

mlflow.register_model(model_info.model_uri, model_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Clean up Classroom
# MAGIC
# MAGIC **🚨 Warning:** Please refrain from deleting the catalog and tables created in this demo, as they are required for upcoming demonstrations. To clean up the classroom assets, execute the classroom clean-up script provided in the final demo.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC In this demo, first, we created a "managed" vector search index using a delta table. After creating the index, we searched for documents similar to the input query. In the second part of the demo, we built and registered the RAG pipeline to Unity Catalog Model Registry. Before registering the model, we enabled mlflow's autolog to trace model run. In the next demos, we will show to evaluate the performance of this model and deploy it into production.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>