# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Agent Components and Use Cases

# COMMAND ----------

# MAGIC %md
# MAGIC ### AI Agent Systems
# MAGIC **Non-agentic (static) workflow**
# MAGIC - Static prompt response or fixed pipelines of hardcoded prompt response systems
# MAGIC - Could also be an API call to another service or ML model.
# MAGIC - Deterministic actions
# MAGIC
# MAGIC **Agentic (dynamic, iterative) workflow**
# MAGIC - Planning and execution by AI
# MAGIC - Tool calling by AI
# MAGIC - Non-deterministic actions
# MAGIC - Iterative workflows
# MAGIC
# MAGIC ![agentvsnon-agent.png](../Includes/images/agentvsnon-agent.png "agentvsnon-agent.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Components of Agentic Systems
# MAGIC **LLM**
# MAGIC - A “brain”--LLM to control the core logic and sequencing of actions the agent executes. It plans the work of the interacting components.
# MAGIC - Other LLMs or AI models as needed for sub-tasks and actions.
# MAGIC
# MAGIC **Tools**
# MAGIC
# MAGIC External resources that the agent uses via tool use or tool calling, e.g., functions, APIs, classic ML models.
# MAGIC
# MAGIC **Memory**
# MAGIC - Short-term session and current conversational state tracking to help with planning and execution of subsequent actions.
# MAGIC - Long-term episodic, semantic, and procedural memory for historical state, knowledge, preferences. 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Common Patterns
# MAGIC ####Pattern: Reasoning
# MAGIC **Chain-of-Thought**
# MAGIC A prompting technique that can be used to illicit reasoning from an instruct model.
# MAGIC
# MAGIC **Reasoning model**
# MAGIC A model that has been trained to automatically determine when to think about a problem.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Pattern: ReAct (Reason + Act)
# MAGIC - Enables models to generate verbal reasoning traces and actions.
# MAGIC - Main states used in a ReAct agent are;
# MAGIC   - **Thought**: Reflect on the problem given and previous actions taken
# MAGIC   - **Act**: Choose the correct tool and input format to use.
# MAGIC   - **Observe**: Evaluate the result of the action and generate next thought.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Pattern: Plan-And-Solve
# MAGIC - Enables models to generate plans and then execute and observe.
# MAGIC - Main components are
# MAGIC   - **Planner**: Reflect on the task and generate a series of steps to complete the task
# MAGIC   - **Execute**: Process step(s) in the generated plan using tools and observations

# COMMAND ----------

# MAGIC %md
# MAGIC ### Use Cases
# MAGIC ![use-cases.png](../Includes/images/use-cases.png "use-cases.png")
# MAGIC
# MAGIC **Intelligent Document Processing**
# MAGIC
# MAGIC With an agentic system, we can extract deep, contextual insights from massive volumes of documents at scale. Think of an agent that doesn't just 'read' a contract, but cross-references clauses against company policy and flags discrepancies automatically.
# MAGIC
# MAGIC **Knowledge Base + Search**
# MAGIC
# MAGIC AI agents transform search systems into dynamic retrieval systems. Instead of giving you a list of links, these agents search through your internal data, synthesize the information, and provide a direct, cited answer. It's the difference between finding a document and finding the actual answer hidden within it.
# MAGIC
# MAGIC **Machine Learning + AI**
# MAGIC
# MAGIC We use classic ML for what it does best—-like predictive analytics and structured data forecasting-—and then use Generative AI agents to interpret those results. They can explain the 'why' to a human user and suggest the next best action.

# COMMAND ----------

# MAGIC %md
# MAGIC ### How Databricks Uses Agents
# MAGIC ![how-databricks-uses-agents.png](../Includes/images/how-databricks-uses-agents.png "how-databricks-uses-agents.png")
# MAGIC
# MAGIC Agents are at the heart of the Databricks Assistant, customer support requests, and the AI/BI Genie.