# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Agent Development Lifecycle
# MAGIC
# MAGIC ![agent-lifecycle.png](../Includes/images/agent-lifecycle.png "agent-lifecycle.png")
# MAGIC
# MAGIC To build agent systems on Databricks we have a comprehensive package of features under Mosaic AI. This set of tools will help you build, deploy, and govern AI agent systems efficiently. 
# MAGIC
# MAGIC Let’s break these features into 4 pillars. 
# MAGIC
# MAGIC - To prepare data, Databricks provides powerful tools like data ingestion, ML features, peer labeling, and vector indexing, enabling high-quality data organization and retrieval for AI applications. 
# MAGIC
# MAGIC - To build agents, you can leverage model tuning, function calling, and the tool catalog, allowing you to create intelligent, fine-tuned AI systems tailored to your needs. 
# MAGIC
# MAGIC - To evaluate agents, tools like LLM judges, lineage tracking, and tracing help monitor performance and optimize workflows. 
# MAGIC
# MAGIC - Deploying agents is seamless with MLOps and agent serving tools, ensuring smooth integration into real-world applications. 
# MAGIC
# MAGIC Governance is built-in with AI guardrails, credential management, usage tracking, and rate limits, ensuring security, compliance, and responsible AI usage.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Model Context Protocol
# MAGIC
# MAGIC ![model-context-protocol.png](../Includes/images/model-context-protocol.png "model-context-protocol.png")
# MAGIC
# MAGIC The best models need data intelligence in the form of access to tools. 
# MAGIC
# MAGIC Anthropic’s Model Context Protocol (MCP) is first-class in Databricks. This means you can build, run, govern your MCP servers inside the Databricks security perimeter. This is going to be huge. And we now have first-class implementations of Databricks in MCP so your agents can interact with DB.