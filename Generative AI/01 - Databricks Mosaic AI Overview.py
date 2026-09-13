# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Databricks Mosaic AI Overview
# MAGIC Generative AI is changing the future of work.
# MAGIC Those who have adopted Generative AI see massive gains in:
# MAGIC
# MAGIC 1. **Innovation**: To build innovation and disruptive customer experiences, executives are investing in Gen AI. In fact 91% of executives in companies with 1B$ or more in revenue are investing in Gen AI already, and this numbers goes to 97% for companies with 10B$ or more in revenue plan to build their own models as part of their GenAI investments (MIT Technology Review). In a different study, 78% of executives surveyed say Gen AI will have high impact on driving innovation 
# MAGIC
# MAGIC 2. **Competitiveness/Revenue**: 75% of CEOs say companies with the most advanced GenAI will have a competitive advantage.  This will lead to increase in revenue. Just in the generative AI assistant market alone, this is a multi-billion dollar addressable market. Generative AI is more than that and the revenue impact across industries will be far greater!
# MAGIC
# MAGIC 3. **Productivity**: We’ve seen dramatic productivity gains with GenAI. A recent study showed that those employees who used GenAI were 40% more productive than those without GenAI. In a different study, developers were able to code faster using ML-based assistants (56% faster). This is the trend we are seeing across many horizontal functions where GenAI can boost productivity of employees to move faster.
# MAGIC
# MAGIC Refer to: [KPMG Generative AI Survey](https://info.kpmg.us/news-perspectives/technology-innovation/kpmg-generative-ai-2023.html) 

# COMMAND ----------

# MAGIC %md
# MAGIC ![every-company.png](./Includes/images/every-company.png "every-company.png")
# MAGIC
# MAGIC Today, every company wants to be a Data+AI company, recognizing that this is the path to competitive advantage. While all organizations are eager to win this race and capture the massive value of AI, the reality is that major hurdles exist. We must acknowledge that there are important challenges preventing most organizations from scaling their AI efforts effectively. Let's look at what those roadblocks are.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Challenges
# MAGIC
# MAGIC ![challenges.png](./Includes/images/challenges.png "challenges.png")
# MAGIC
# MAGIC In the first example, we have a customer chatbot for Chevy, powered by CHatGPT, that, when asked “What is the best truck?”, responds with Ford F-150, their competitors product. What’s going on here?  The model is lacking enterprise context and guidance on how to respond when asked about competitors, and there are no guardrails in place. Not Accurate.
# MAGIC
# MAGIC In the second example, we have Air Canada who built a chatbot that hallucinated on a response to a customer and gave the wrong answer on their bereavement policy leading to the company needing to honor financially what the bot told the customer. 
# MAGIC
# MAGIC In the third example, we have a customer chatbot that retrieves information from a database to respond to a customer. Henry tells the chatbot his phone plan is too expensive. The agent then retrieves private information about Henry’s co-worker, Heather. Without governance over the underlying data, incidents like these are inevitable. The model cannot know the governance context of your customer. It needs rules to know that sharing a co-worker's data is a privacy breach, even if sharing family member data might be allowed.
# MAGIC
# MAGIC Refer to: [WIRED](https://www.wired.com/story/air-canada-chatbot-refund-policy/)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Difficult and Expensive
# MAGIC ![difficult.png](./Includes/images/difficult.png "difficult.png")
# MAGIC
# MAGIC Bringing GenAI to production is difficult. While many organizations have built POCs (proof of concepts) with LLMs, they are struggling to move them to production. The challenges they face include: unpredictable performance (current LLMs have risks of undesirable model outputs such as hallucinations and toxicity). Customers want consistent, accurate responses that are based on their data (only). There also is a challenge of automation and scale. Customers need to think about the entire ML lifecycle (from data prep, to experimentation, and operationalization) and currently lack access controls for governance, auditability / traceability and regulatory compliance.
# MAGIC
# MAGIC GenAI can also be unnecessarily difficult and expensive because you do not have control over the data or the models. Everyone is using the same SaaS models, which means organizations must send their enterprise data to the SaaS provider who owns and controls the model.
# MAGIC
# MAGIC Too expensive at scale: Organizations who are building their own models (fine-tune or pre-train), want to achieve the same quality of models as OpenAI and ChatGPT for their domains, but at an accessible cost. 
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## The Data Lakehouse
# MAGIC ![lakehouse.png](./Includes/images/lakehouse.png "lakehouse.png")
# MAGIC
# MAGIC At its heart, the Databricks Data Intelligence Platform is built on the foundation of the Lakehouse Architecture. This paradigm takes the best aspects of data lakes and data warehouses and merges them into a single, unified, open platform.
# MAGIC
# MAGIC The foundation is your open data lake, where Delta Lake provides the unified formatting layer, ensuring reliability and ACID transactions for all your data. Layered on top of that is Unity Catalog, which provides a simple, unified governance layer. This is how we maintain security, compliance, and lineage across your entire data ecosystem.
# MAGIC
# MAGIC Crucially, the platform supports all your data teams under one roof—from Data Engineering to BI, and ML to GenAI. It provides practitioners with all the unique, specialized tools they need, while also being simple and easy to use for both technical and non-technical professionals.
# MAGIC The entire system is secure by default and includes a complete, integrated suite of tools specifically designed to accelerate your Generative AI development.
# MAGIC
# MAGIC The Lakehouse architecture has already become a major force in the market. But at the same time, we've seen another technology rise even more rapidly: Generative AI.
# MAGIC
# MAGIC To truly capture the potential of AI, combining the reliability and governance of the data lakehouse with the power of Generative AI is essential. This integration is what creates a truly strong and intelligent platform.
# MAGIC
# MAGIC At Databricks, we’ve brought these two technologies together to create an entirely new category of data platform: The Data Intelligence Platform.
# MAGIC
# MAGIC This unified approach opens up a whole new world of possibilities, allowing us to successfully democratize data and AI across the entire organization.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Build Better on Databricks
# MAGIC ![build-better.png](./Includes/images/build-better.png "build-better.png")
# MAGIC
# MAGIC Databricks empowers organizations to productionize their GenAI models cost-effectively using their own data. We deliver three key advantages:
# MAGIC
# MAGIC - **Production Quality**: You get faster, more reliable deployment. This means accurate, safe, and governed GenAI applications that meet enterprise standards.
# MAGIC
# MAGIC - **Complete Control**: You retain full ownership over both the models and the data. With Unity Catalog, you have total governance and security of all your AI assets.
# MAGIC
# MAGIC - **Lower Cost**: Our optimized platform allows you to build and deploy LLMs at scale for low costs, maximizing your investment in innovation.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Databricks Enables Every Architectural Pattern
# MAGIC ![every-pattern.png](./Includes/images/every-pattern.png "every-pattern.png")
# MAGIC
# MAGIC The real power of Databricks is that we are the only provider that can enable the entire architectural spectrum for Generative AI. We handle everything from the simplest interactions to the most complex, custom models. This spans five key areas:
# MAGIC
# MAGIC 1. **Prompt Engineering**: This is the foundational skill—crafting specialized prompts to guide the Large Language Model's behavior to get the output you need.
# MAGIC
# MAGIC 2. **Deterministic Agentic Systems**: These are reliable agents where the behavior is entirely predictable, based on initial conditions and a defined set of rules.
# MAGIC
# MAGIC 3. **Autonomous Agentic Systems**: This is the next level. These are non-deterministic systems where the agent’s behavior includes an element of self-determination or advanced reasoning.
# MAGIC
# MAGIC 4. **Fine-Tuning**: If you need to adapt an existing, pre-trained LLM to your specific data sets or proprietary domains, we provide the tools for efficient fine-tuning.
# MAGIC
# MAGIC 5. **Pre-Training**: And finally, for maximum differentiation, we enable you to train a custom LLM from scratch, giving you complete control over your foundational model.
# MAGIC
# MAGIC No other platform offers this complete, end-to-end capability.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>