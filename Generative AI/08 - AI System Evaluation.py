# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # AI System Evaluation
# MAGIC Evaluating AI systems before deployment is a critical safeguard against technical, ethical, and operational risks that can have real-world consequences. Unlike traditional software, Generative AI is non-deterministic, meaning it can produce unexpected outputs, even when given identical inputs. Comprehensive evaluation can identify these failures early, ensuring that the system is not only accurate and grounded in fact but also cost effective.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Evaluating the Whole System
# MAGIC When we work with generative AI, we must recognize that we are not just deploying a single model; we are building a complex system.
# MAGIC A solution like RAG, for example, is a pipeline that includes data preparation and a vital retrieval component to bring in external, proprietary context. When evaluating these systems, we have to align our metrics directly with business goals
# MAGIC
# MAGIC - Cost metrics
# MAGIC
# MAGIC     - Resources -- A major component of cost is the resources involved to create and deploy the GenAI system.
# MAGIC
# MAGIC     - Time -- Cost also includes the time and engineering effort required to operate the system reliably in production.
# MAGIC
# MAGIC - Performance
# MAGIC     - Direct value -- Performance is about whether the system actually provides value to customers directly, through explicit user feedback.
# MAGIC
# MAGIC     - Indirect value -- We can also measure performance indirectly by analyzing usage and behavioral data.
# MAGIC
# MAGIC - Custom metrics for your own use case
# MAGIC     - Defining custom metrics is often the hardest, but also the single most important step in successfully building a robust, high-value generative AI application.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Evaluating Individual Components
# MAGIC When evaluating RAG solutions, we need to evaluate each component separately and together.
# MAGIC
# MAGIC Components to evaluate (and that can be adjusted):
# MAGIC
# MAGIC - Chunking 
# MAGIC
# MAGIC     - Method (senantic, fixed-size)
# MAGIC
# MAGIC     - Size
# MAGIC
# MAGIC - Embedding model
# MAGIC
# MAGIC - Vector store
# MAGIC
# MAGIC - Retrieval method and re-ranker
# MAGIC
# MAGIC - Generator

# COMMAND ----------

# MAGIC %md
# MAGIC ## Evaluation Metrics
# MAGIC
# MAGIC ![evaluation-diagram.png](./Includes/images/evaluation-diagram.png "evaluation-diagram.png")
# MAGIC As we discuss the metrics below, consult the diagram above:
# MAGIC
# MAGIC - **Context Precision**:
# MAGIC
# MAGIC     - Based on the relationship between the **query** and the retrieved **context**.
# MAGIC
# MAGIC     - Assesses whether the chunks/nodes in the retrieval context ranked higher than irrelevant ones.
# MAGIC
# MAGIC - **Context Relevance**:
# MAGIC     
# MAGIC     - Also based on the relationship between the **query** and the retrieved **context**.
# MAGIC     
# MAGIC     - Measures how relevant the retrieved context is to the query.
# MAGIC
# MAGIC     - This metric does not assess factual accuracy but focuses on how well the context supports answering the given question.
# MAGIC
# MAGIC - **Context Recall**:
# MAGIC     
# MAGIC     - Based on **ground truth** and retrieved **context**.
# MAGIC     
# MAGIC     - Measures the extent to which all relevant entities and information are retrieved and mentioned in the context provided.
# MAGIC     
# MAGIC - **Faithfulness**:
# MAGIC     
# MAGIC     - Based on the **response** and retrieved **context**.
# MAGIC     
# MAGIC     - Measures the factual accuracy of the generated answer in relation to the provided context.
# MAGIC     
# MAGIC - **Answer Relevancy**:
# MAGIC     
# MAGIC     - Based on the alignment of the **response** with the user's **query**.
# MAGIC     
# MAGIC     - Assesses how pertinent and applicable the generated response is to the user's initial query. 
# MAGIC     
# MAGIC - **Answer Correctness**:
# MAGIC
# MAGIC     - Based on the **ground truth** and the **response**.
# MAGIC
# MAGIC     - Measures the accuracy of the generated answer when compared to the ground truth.
# MAGIC
# MAGIC     - Encompasses both semantic and factual similarity with the ground truth.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Human Feedback
# MAGIC - Often developers are not the experts of the domain
# MAGIC
# MAGIC - Models’ output need to be evaluated by human experts
# MAGIC
# MAGIC - Models’ outputs and associated feedback need to be collected and stored in a structured manner
# MAGIC
# MAGIC - Feedback can be explicit or implicit:
# MAGIC
# MAGIC     - Explicit feedback: Direct and intentional input from users. Such as ratings, comments and review.
# MAGIC
# MAGIC     - Implicit feedback: Gathered indirectly by observing user behavior and interactions. Such as engagement metrics and behavioral data.
# MAGIC
# MAGIC Databricks provides excellent methods of collecting [human feedback](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/)

# COMMAND ----------

# MAGIC %md
# MAGIC ## MLflow Scorers & LLM Judges in Databricks
# MAGIC By leveraging [MLflow Scorers and LLM-as-a-Judge](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/scorers) within the Databricks platform, you can automate the assessment of non-deterministic model outputs, ensuring that generative applications remain grounded, safe, and aligned with enterprise standards at scale.
# MAGIC
# MAGIC - **Scorers** -- A universal interface for quality. Whether you are building a simple chatbot or a complex RAG agent, Scorers give you a standardized way to define what 'good' looks like.
# MAGIC
# MAGIC There are four types of scorers:
# MAGIC
# MAGIC - **Built-in Judges**: Out-of-the-box research-validated metrics (e.g., Groundedness, Safety).
# MAGIC
# MAGIC - **Guidelines Judges**: Checking responses against natural language rules (e.g., "Tone should be professional").
# MAGIC
# MAGIC - **Custom Judges**: Specialized LLM-based evaluation with bespoke rubrics and score ranges.
# MAGIC
# MAGIC - **Code-based Scorers**: Deterministic metrics (e.g., Exact Match, Regex, JSON schema validation).
# MAGIC
# MAGIC **LLMs as Judges** -- Used to evaluate many common metrics.
# MAGIC
# MAGIC - **RetrievalGroundedness**: Detects hallucinations by checking if the response stays faithful to the context.
# MAGIC
# MAGIC - **RelevanceToQuery**: Measures how well the response addresses the user’s specific request.
# MAGIC  
# MAGIC - **Correctness**: Compares the model output against a "Ground Truth" (Requires expectations data).
# MAGIC  
# MAGIC - **Safety**: Flags harmful, offensive, or toxic content.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Monitoring Quality in Production
# MAGIC Here are some recommendations for running quality checks after your model is deployed to production:
# MAGIC
# MAGIC - Automatically run MLflow scorers on traces from your production GenAI apps to continuously monitor quality.
# MAGIC
# MAGIC - Use the same scorers in development and production to ensure consistent evaluation.
# MAGIC
# MAGIC - Continuous quality assessment with monitoring running in the background.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>