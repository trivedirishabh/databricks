# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Welcome to the Course!
# MAGIC ## Important Note:
# MAGIC This course will run in Databricks Free Edition. However, please note that, in the course notebooks, we will be deploying a vector search index, which requires a vector search endpoint, and we will be deploying a finished model to Mosaic AI Model Serving. Databricks Free Edition has caps on the number of vector search endpoints and model serving endpoints you can deploy. If you run into errors in any of the notebooks that deploy this infrastructure, please double-check that you have not hit these caps.

# COMMAND ----------

# MAGIC %md
# MAGIC # Agents and Agent Patterns

# COMMAND ----------

# MAGIC %md
# MAGIC ## What is an Agent?
# MAGIC An AI agent is an intelligent application that uses an AI model and other tools to iteratively plan and execute sequences of actions to complete a complex task.
# MAGIC - Agents automate processes that previously only humans could do
# MAGIC - Agents do this by prompting an LLM to reason about what data or APIs or other Agents should be used to effectively respond to a user’s request
# MAGIC - Agent ROI is usually calculated by “# of human hours saved”
# MAGIC ![what-is-an-agent.png](../Includes/images/what-is-an-agent.png "what-is-an-agent.png")
# MAGIC
# MAGIC If a human called a customer service line and asked, "Can you help me return my last order", what would a human do?

# COMMAND ----------

# MAGIC %md
# MAGIC ## Human Process
# MAGIC ![agent-workflow.png](../Includes/images/agent-workflow.png "agent-workflow.png")
# MAGIC
# MAGIC A human would reason about what to do, find relevant information, and take an action

# COMMAND ----------

# MAGIC %md
# MAGIC ## Agent Process
# MAGIC ![agent-process.png](../Includes/images/agent-process.png "agent-process.png")
# MAGIC
# MAGIC An agent does the same thing except it uses an LLM to reason, find information, and take actions

# COMMAND ----------

# MAGIC %md
# MAGIC ## Fitting AI Agents into Broader AI Systems
# MAGIC **AI systems** - encompass any software that utilizes machine learning models to function.
# MAGIC
# MAGIC **Compound AI Systems** - interact with external components—-like databases, search engines, or other APIs—-to deliver a more reliable and factual output.
# MAGIC
# MAGIC **Agentic AI** - the environment or the strategy that orchestrates agent workers. When we talk about Agentic AI, we are usually referring to Multi-Agent Systems. This is where multiple specialized agents collaborate, peer-review each other, and execute complex workflows without constant human hand-holding.
# MAGIC
# MAGIC **AI Agents** - the individual 'workers.' They are defined by four specific capabilities: they have an AI model as a brain, planning capabilities to break down tasks, memory to track progress, and the ability to use tools (like running code or searching a file).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Multi-Agent Systems
# MAGIC In a multi-agent system, a type of Agent, called a supervisor (or moderator/ or router) combines multiple Agents together.  
# MAGIC
# MAGIC The supervisor:
# MAGIC - Uses an LLM to decide which agent should speak next
# MAGIC - Deterministically passes the conversation history to that agent (e.g., via code, no LLM regurgitating the tokens)
# MAGIC - Lets that agent respond
# MAGIC - Based on that response + conversation history, decides to either loop through the process again or return the output to the user

# COMMAND ----------

# MAGIC %md
# MAGIC ## Definitions
# MAGIC **Conversational Agents**: A conversational agent (chat agent, chatbot) is designed for iterative collaboration with humans and other agents through multi-turn conversations, where the conversation history is maintained somewhere. They don't just talk; they reason and act based on a continuous stream of context. They transform a simple text box into a functional interface for complex tasks.
# MAGIC
# MAGIC **Tool**: A specific function that an AI model uses to perform a task. The details needed for the function (called parameters) are selected by the AI itself. A tool is designed to complete a specific task in a single step.
# MAGIC
# MAGIC **Tool Calling Agent**: (aka, "Function Calling Agent") An Agent that has a set of Tools.  The Agent uses an LLM to:
# MAGIC - Reason about which Tool(s) to call
# MAGIC - Call those tools
# MAGIC - Reason about tool output and either call additional Tool(s) or respond to the user