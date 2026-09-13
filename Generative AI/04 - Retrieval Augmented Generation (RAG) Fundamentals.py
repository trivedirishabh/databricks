# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Retrieval Augmented Generation (RAG) Fundamentals
# MAGIC
# MAGIC Retrieval Augmented Generation, or RAG:
# MAGIC - Is a pattern that can improve the efficacy of large language model (LLM) applications by leveraging custom data.
# MAGIC
# MAGIC - Is done by retrieving data/documents relevant to a question or task and providing them as context to augment the prompts to an LLM to improve generation.
# MAGIC
# MAGIC The main problem that is solved with RAG architecture is the knowledge gap. This approach enhances the accuracy and relevance of responses.
# MAGIC
# MAGIC Common use cases:
# MAGIC - Q&A Chatbots:  Derive more accurate answers by using internal information sources.
# MAGIC
# MAGIC - Search Augmentation: Augment search results with LLM-generated answers.
# MAGIC
# MAGIC - Content Creation and Summarization: Develop high-quality articles, reports, and summaries using additional context.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Benefits of a RAG Architecture
# MAGIC - Up-to-date and accurate responses
# MAGIC     - LLM responses are not based solely on static training data.
# MAGIC     - The model uses **up-to-date external data** sources to provide responses.
# MAGIC - Reducing inaccurate responses, or hallucinations
# MAGIC     - RAG attempts to mitigate the risk of producing “**hallucinations**” or incorrect information.
# MAGIC     - Outputs can include citations of **original sources**, allowing human verification.
# MAGIC - Domain-specific contextualization
# MAGIC     - Can be tailored to interface with **proprietary or domain-specific data**.
# MAGIC     - Improves the accuracy of the response by using contextually relevant information.
# MAGIC - Efficiency and cost-effectiveness
# MAGIC     - Offers an alternative to fine-tuning LLMs by enabling in-context learning **without the up-front overhead of fine-tuning**.
# MAGIC     - Beneficial where models need to be frequently updated with new data.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sample RAG Architecture
# MAGIC ![sample-rag.png](./Includes/images/sample-rag.png "sample-rag.png")
# MAGIC
# MAGIC - **User Prompt**: The process begins with a user query or prompt. This input serves as the foundation for what the RAG system aims to retrieve.
# MAGIC
# MAGIC - **Embedding conversion**: The user’s prompt is transformed into a high-dimensional vector (or embedding). This representation captures the semantic essence of the prompt and is used to search for relevant information in the database.
# MAGIC
# MAGIC - **Information retrieval**: Using the prompt’s vector representation, RAG queries the external data sources or databases. A vector database can be particularly effective here, allowing for efficient and accurate data fetching based on similarity measures.
# MAGIC
# MAGIC - **Context augmentation**: Relevant information is retrieved and added to the initial prompt, giving the LLM extra context to generate a more informed response.
# MAGIC
# MAGIC - **Response Generation**: The model uses the augmented context to generate a relevant response.
# MAGIC
# MAGIC - **Feedback Loop**: Some RAG implementations might encompass a multi-hop feedback mechanism. In cases where the response is deemed unsatisfactory, the system can revisit its search criteria, tweak the context, or even refine its retrieval strategy, subsequently generating a new answer.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Main Concepts of a RAG Architecture
# MAGIC - **Index & Embed**:
# MAGIC     - An embedding model used for creating vector representation of the documents and user queries.
# MAGIC - **Vector Store**:
# MAGIC     - Specialized to store unstructured data indexed by vectors. Vectors can be stored with a vector DB, library, or plugin.
# MAGIC - **Retrieval**:
# MAGIC     - Search stored vectors using similarity search to efficiently retrieve relevant information.
# MAGIC
# MAGIC - **Filtering & Reranking**:
# MAGIC     - The process of selecting or ranking retrieved documents before passing as context. 
# MAGIC
# MAGIC - **Prompt Augmentation**:
# MAGIC     - Prompt engineering workflow to enhance context via injection of data retrieved from a vector store.
# MAGIC
# MAGIC - **Generation**:
# MAGIC     - A large language model used for generating a response for the user’s request.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>