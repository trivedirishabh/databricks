-- Databricks notebook source
-- MAGIC %md
-- MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # GenAI Model Deployment
-- MAGIC Databricks provides production-ready serving systems for GenAI apps, agents, and models backed by Databricks Apps and Model Serving. These scalable deployments can be used for both real-time serving and batch inference. All deployments integrate with observability and evaluation and monitoring tooling.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ![latency-throughput.png](./Includes/images/latency-throughput.png "latency-throughput.png")
-- MAGIC Here are three deployment paradigms:
-- MAGIC
-- MAGIC - **Batch inference**: Involves computing predictions ahead of time and storing them for later use. It offers high throughput but comes with higher latency, making it suitable for use cases like summarizing long-form text into informative documents. 
-- MAGIC
-- MAGIC - **Streaming inference**: Processes predictions as features arrive and stores them, delivering medium latency and medium throughput. This works well for scenarios such as translating product reviews before publication. 
-- MAGIC
-- MAGIC - **Real-time inference**: Generates predictions immediately upon request, offering low latency but lower throughput. It is often used in interactive applications like deployed RAG systems, though real-time endpoints can also be leveraged for batch inferencing in GenAI workloads.
-- MAGIC
-- MAGIC Note that the deployment paradigm you choose affects both latency and throughput
-- MAGIC
-- MAGIC - **Latency**: The time it takes to complete a request.
-- MAGIC
-- MAGIC - **Throughput**: Refers to the throughput per GPU or machine, meaning that high-throughput real-time serving can still be achieved by scaling across multiple machines-—a concept known as concurrency in Databricks Model Serving. 
-- MAGIC
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Mosaic AI as a Solution
-- MAGIC
-- MAGIC Deploying real-time AI is a major hurdle for many organizations, with the primary challenges centered around infrastructure, tool fragmentation, and specialized resource requirements. Real-time systems demand fast, scalable serving infrastructure that is both costly to build and difficult to maintain. Furthermore, data teams often struggle with disparate tools for development versus deployment, leading to increased complexity and costs as they navigate separate platforms for data, LLMs, and serving. Finally, the steep learning curve of deployment tools creates a bottleneck where limited engineering resources restrict the ability to scale AI effectively across the enterprise.
-- MAGIC
-- MAGIC ![mosaic-ai-model-serving.png](./Includes/images/mosaic-ai-model-serving.png "mosaic-ai-model-serving.png")
-- MAGIC
-- MAGIC Mosaic AI Model Serving directly addresses the challenges of deploying real-time AI by providing Production-Grade Serving that is highly available, low latency, and scalable for both small and large workloads. By leveraging Lakehouse-Unified Serving, the platform accelerates deployments through automatic feature lookups, integrated monitoring, and unified governance, which effectively automates deployment and reduces manual errors. This approach replaces fragmented, disparate tools with a simplified deployment model, offering developers the flexibility to integrate models into websites and applications via a user-friendly UI or a robust API.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Databricks Mosaic AI Model Serving
-- MAGIC
-- MAGIC ![model-serving-capabilities.png](./Includes/images/model-serving-capabilities.png "model-serving-capabilities.png")
-- MAGIC
-- MAGIC Databricks Mosaic AI Model Serving provides a unified interface, including a single API, SDK, and UI, to manage, govern, and monitor all types of AI models in one centralized location. The platform enables seamless access to a wide range of architectures, including custom agents and chains, Databricks-hosted foundation models like Gemini, Llama and those from OpenAI and Anthropic. By streamlining how these diverse models are queried and overseen, the system simplifies the operational complexity of supporting a modern AI stack.
-- MAGIC
-- MAGIC - **Usage tracking and observability**: Monitor who’s using models and how often to help optimize performance and manage costs.
-- MAGIC
-- MAGIC - **Payload logging**: Capture requests and responses in Unity Catalog, allowing you to debug and improve model quality.
-- MAGIC
-- MAGIC - **Unified Guardrails**: A single source of truth for data policies, with guardrails like PII detection to ensure compliance. 
-- MAGIC
-- MAGIC - **A/B testing and traffic policies**: Fallback/retry policies.
-- MAGIC
-- MAGIC - **Permissions and granular rate limiting**: Only authorized users can access models and APIs, while controlling the number of requests to optimize performance.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>