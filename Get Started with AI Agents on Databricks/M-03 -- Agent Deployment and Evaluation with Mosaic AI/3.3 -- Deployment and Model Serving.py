# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Deployment and Model Serving

# COMMAND ----------

# MAGIC %md
# MAGIC ### Deployment Paradigms
# MAGIC
# MAGIC ![three-paradigms.png](../Includes/images/three-paradigms.png "three-paradigms.png")
# MAGIC
# MAGIC The deployment of Generative AI follows paradigms similar to traditional machine learning, primarily categorized by the trade-off between latency and throughput. As you move from batch processing to real-time execution, latency decreases significantly, allowing for faster individual responses. However, this shift typically results in a decrease in overall throughput, as the system moves from processing large volumes of data simultaneously to handling individual requests.
# MAGIC
# MAGIC **Batch deployment** focuses on high-volume processing where completions are generated and stored for an entire table of text inputs or prompts at once. 
# MAGIC
# MAGIC **Streaming deployment** acts as a middle ground, generating and storing completions on micro-batches of inputs as they are processed in near-real-time. These methods are ideal for background tasks where immediate user interaction is not required but large datasets must be processed efficiently.
# MAGIC
# MAGIC **Real-time deployment** is designed for interactive applications where completions are generated asynchronously and instantly for individual inputs or prompts. This paradigm is essential for the conversational agents and multi-agent systems we have discussed, ensuring that the AI can respond to user queries with the lowest possible latency.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mosaic AI as a Solution
# MAGIC
# MAGIC Deploying real-time AI is a major hurdle for many organizations, with the primary challenges centered around infrastructure, tool fragmentation, and specialized resource requirements. Real-time systems demand fast, scalable serving infrastructure that is both costly to build and difficult to maintain. Furthermore, data teams often struggle with disparate tools for development versus deployment, leading to increased complexity and costs as they navigate separate platforms for data, LLMs, and serving. Finally, the steep learning curve of deployment tools creates a bottleneck where limited engineering resources restrict the ability to scale AI effectively across the enterprise.
# MAGIC
# MAGIC ![mosaic-ai-model-serving.png](../Includes/images/mosaic-ai-model-serving.png "mosaic-ai-model-serving.png")
# MAGIC
# MAGIC Mosaic AI Model Serving directly addresses the challenges of deploying real-time AI by providing Production-Grade Serving that is highly available, low latency, and scalable for both small and large workloads. By leveraging Lakehouse-Unified Serving, the platform accelerates deployments through automatic feature lookups, integrated monitoring, and unified governance, which effectively automates deployment and reduces manual errors. This approach replaces fragmented, disparate tools with a simplified deployment model, offering developers the flexibility to integrate models into websites and applications via a user-friendly UI or a robust API.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Databricks Model Serving
# MAGIC
# MAGIC ![model-serving-capabilities.png](../Includes/images/model-serving-capabilities.png "model-serving-capabilities.png")
# MAGIC
# MAGIC Databricks Model Serving provides a unified interface, including a single API, SDK, and UI, to manage, govern, and monitor all types of AI models in one centralized location. The platform enables seamless access to a wide range of architectures, including custom agents and chains, Databricks-hosted foundation models like Gemini and Llama, and third-party external models such as those from OpenAI and Anthropic. By streamlining how these diverse models are queried and overseen, the system simplifies the operational complexity of supporting a modern AI stack.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Collecting Feedback
# MAGIC
# MAGIC With Databricks Model Serving, you can set up Human in the Loop feedback that is logged to Unity Catalog for building a golden, labeled dataset and fine-tuning.
# MAGIC
# MAGIC You can also easily setup a review app that provides a pre-built chat app, which makes it easy to collect feedback from SMEs.
# MAGIC
# MAGIC You can use Agent Evaluation and AI/BI dashboards to pinpoint quality issues based on LLM judges and user feedback.
# MAGIC
# MAGIC Finally, you can monitor many metrics online, which allows you to continuously validate quality and performance, quickly fix issues, and unify observability.