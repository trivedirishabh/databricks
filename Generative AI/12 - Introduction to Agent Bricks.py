# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Introduction to Agent Bricks
# MAGIC Agent Bricks offers a streamlined approach for both technical and non-technical teams to operationalize their data into production-grade AI agents. Declarative agents can be built and refined using natural language and pre-configured templates for tasks like information extraction, knowledge assistance, and multi-agent coordination.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Challenges for Building GenAI Systems
# MAGIC - How do you adapt AI systems to your needs?
# MAGIC
# MAGIC     - LLMs do not understand enterprise data well enough 
# MAGIC
# MAGIC     - Prompt engineering is often based on “vibe checks”
# MAGIC
# MAGIC     - Too many tools/components to research and integrate
# MAGIC
# MAGIC - How do you get to the right quality?
# MAGIC
# MAGIC     - Lack of labeled data 
# MAGIC
# MAGIC     - Missing verifiable custom evaluations
# MAGIC
# MAGIC - Does the ROI make sense?
# MAGIC
# MAGIC     - Larger models are expensive 
# MAGIC
# MAGIC     - Will end users keep using the product? 
# MAGIC     
# MAGIC     - Does the output quality justify the cost? 

# COMMAND ----------

# MAGIC %md
# MAGIC ## The Current GenAI Market
# MAGIC ![agent-bricks-matrix.png](./Includes/images/agent-bricks-matrix.png "agent-bricks-matrix.png")
# MAGIC
# MAGIC Let’s frame the current GenAI market using a simple matrix based on how easy a product is to build versus the quality it delivers.
# MAGIC
# MAGIC On one hand, many simple no-code one-click builders are easy to use, but they often produce agents with lower quality.
# MAGIC
# MAGIC On the other hand, to achieve truly high quality, you traditionally have to build your own DIY agents. This involves manually prompting models and painstakingly assembling every component, which is incredibly complex and requires significant engineering investment.
# MAGIC
# MAGIC Agent Bricks changes this trade-off. Its goal is to deliver a platform that is both easy to use and can produce incredibly high-quality, production-ready agents.
# MAGIC
# MAGIC Under the hood, Agent Bricks is backed by all the amazing, cutting-edge research from our Mosaic AI research team.
# MAGIC
# MAGIC This includes advanced capabilities like Test-time Adaptive Optimization, the ability to implement custom judges for evaluation, and sophisticated agent deep research workflows.
# MAGIC
# MAGIC The key takeaway is this: we've taken all of this highly advanced technology and packaged it behind a product surface that is incredibly intuitive, making state-of-the-art Generative AI easy for any team to use.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Agent Bricks as a Solution
# MAGIC ![agent-bricks.png](./Includes/images/agent-bricks.png "agent-bricks.png")
# MAGIC
# MAGIC Under the hood, Agent Bricks is backed by all the amazing, cutting-edge research from our Mosaic AI research team.
# MAGIC
# MAGIC This includes advanced capabilities like Test-time Adaptive Optimization, the ability to implement custom judges for evaluation, and sophisticated agent deep research workflows.
# MAGIC
# MAGIC The key takeaway is this: we've taken all of this highly advanced technology and packaged it behind a product surface that is incredibly intuitive, making state-of-the-art Generative AI easy for any team to use.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Agent Bricks
# MAGIC The steps to deploy a GenAI application are easy:
# MAGIC
# MAGIC 1. Select a task and declare a high-level description of the agent
# MAGIC
# MAGIC 2. Agent Bricks:
# MAGIC
# MAGIC     - Creates evaluation benchmarks
# MAGIC
# MAGIC     - Auto-optimizes the agent
# MAGIC
# MAGIC     - Cost and Quality
# MAGIC
# MAGIC 3. Deploy and iterate on quality

# COMMAND ----------

# MAGIC %md
# MAGIC ## Agent Bricks Use Cases
# MAGIC - **Information Extraction**
# MAGIC
# MAGIC     This capability provides an optimized, end-to-end pipeline specifically designed to securely extract insights, entities, and relationships from various documents and complex unstructured data sources. This moves us beyond simply summarizing text and allows us to derive structured, actionable intelligence from documents like contracts, financial reports, or logs.
# MAGIC
# MAGIC - **Knowledge Assistant**
# MAGIC
# MAGIC     This is our specialized framework for building high-quality Question and Answering (Q&A) agents that operate over your specific enterprise knowledge sources, such as internal documents, manuals, or research papers. This task is the backbone for creating highly accurate, grounded RAG applications, ensuring the agent provides reliable answers based on your private data.
# MAGIC
# MAGIC - **Multi-Agent Supervisor**
# MAGIC
# MAGIC     This is the key to building truly complex, intelligent systems. The Supervisor is able to stitch together multiple specialized agents, external tools like MCP servers, and even Genie agents—which are your natural language SQL experts—into a single, cohesive, production-ready system.
# MAGIC
# MAGIC     This orchestrator handles the delegation, coordination, and synthesis of information, allowing you to tackle questions and workflows that no single AI model could ever handle on its own.
# MAGIC
# MAGIC - **Custom LLM**
# MAGIC
# MAGIC     This is designed for more complex and lower-level needs, such as highly-specific content generation or building a dedicated custom chat experience.
# MAGIC
# MAGIC
# MAGIC     In this scenario, you are using the Agent Bricks framework to manage and optimize models that you have either fine-tuned or pre-trained yourself. This gives you the ultimate control to tailor a model’s behavior for proprietary tasks where maximum accuracy and domain specialization are required.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
