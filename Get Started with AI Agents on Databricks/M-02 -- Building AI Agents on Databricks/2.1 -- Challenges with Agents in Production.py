# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](../Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ### The Path to Production is Hard
# MAGIC
# MAGIC ![path-to-production.png](../Includes/images/path-to-production.png "path-to-production.png")
# MAGIC
# MAGIC Putting agent systems into production can be quite difficult for a number of reasons:
# MAGIC
# MAGIC - Many organizations do not have control over the data or the models. Many organizations are using the same SaaS models, which means organizations must send their enterprise data to the SaaS provider, who owns and controls the model.
# MAGIC
# MAGIC - Bringing GenAI to production is difficult. While many organizations have built POCs (proof of concepts) with LLMs, they are struggling to move them to production. The challenges they face include unpredictable performance  because current LLMs have risks of undesirable model outputs such as hallucinations and toxicity. Customers want consistent, accurate responses that are based on their data only. There also is a challenge of automation and scale. Customers need to think about the entire ML lifecycle (from data prep, to experimentation, and operationalization) and currently lack access controls for governance, auditability / traceability and regulatory compliance.
# MAGIC
# MAGIC - Too expensive at scale: Organizations who are building their own models (fine-tune or pre-train), want to achieve the same quality of models as OpenAI and ChatGPT for their domains, but at an accessible cost.
# MAGIC
# MAGIC The winners will have to make this shift and put Gen AI projects into production.  But most companies are not able to move Gen AI into production
# MAGIC Why are they struggling?  It turns out moving from experiments to production deployments is really hard.

# COMMAND ----------

# MAGIC %md
# MAGIC ### General Intelligence Fails for Enterprise Use Cases
# MAGIC
# MAGIC ![gen-intelligence.png](../Includes/images/gen-intelligence.png "gen-intelligence.png")
# MAGIC
# MAGIC AI innovation is happening at an unprecedented pace.  We routinely see new foundation models release every month that set new records in academic benchmarks.  However, these models are built for General Intelligence. This means they are trained using a broad dataset from the Internet that is disconnected from your enterprise data. This does not work for your enterprise use cases, because you need your AI applications to understand your enterprise data.  This is one of the main reasons why organizations have not deployed GenAI into production quickly. Enterprises have low confidence in getting consistently high-quality outputs, especially because of hallucinations caused by a disconnect from enterprise data.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mosaic AI enables you to build production-quality, enterprise-ready Agents faster
# MAGIC
# MAGIC ![mosaic-ai-benefits.png](../Includes/images/mocaic-ai-benefits.png "mosaic-ai-benefits.png")
# MAGIC
# MAGIC Complete Control: Complete ownership over both the models and the data 
# MAGIC - Own the GenAI models, securely trained by your enterprise data
# MAGIC - Increased privacy and reduced reputational risk
# MAGIC
# MAGIC Production quality: Faster, more reliable deployment across multiple use cases
# MAGIC - Only platform with native evaluation, monitoring and governance 
# MAGIC - Standardized operations
# MAGIC
# MAGIC Lower cost: You can build LLMs at scale for low costs
# MAGIC - Up to 90% less expensive for RAG
# MAGIC - Up to 90% cheaper to train your own LLMs

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mosaic AI Works Natively with Unity Catalog
# MAGIC
# MAGIC ![data-intelligence.png](../Includes/images/data-intelligence.png "data-intelligence.png")
# MAGIC
# MAGIC
# MAGIC 1. Unified Formats: The End of Ecosystem Lock-in
# MAGIC
# MAGIC     The foundation of working with Agent systems is the storage layer. Databricks fundamentally changed the game by unifying data formats. By removing the friction between formats, no one in your organization ever has to worry about 'format ecosystems' again. You write your data once, and it is accessible to every engine in your stack without expensive replication or translation.
# MAGIC
# MAGIC 2. Agents in Unity Catalog
# MAGIC
# MAGIC     Unity Catalog sits directly at the center of the architecture, governing everything from raw data to the AI models and Mosaic AI tools we discussed earlier. A system is only as good as its governance, and Unity Catalog provides that 'single pane of glass' for discovery, audit, and lineage across your entire estate.
# MAGIC
# MAGIC 3. The Most Open Catalog in the Industry
# MAGIC
# MAGIC     Unity Catalog is the most open catalog in the industry. We have fully open-sourced the Unity Catalog protocol, ensuring it is compatible with open standards like the Iceberg REST API. This openness means your metadata isn't trapped in a proprietary black box. It allows for a truly interoperable Data Intelligence Platform where your data, your governance, and your AI agents can all communicate seamlessly, regardless of which cloud or tool you choose to use.