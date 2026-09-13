# Databricks notebook source
# MAGIC %md
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Using the Databricks Data Science Agent
# MAGIC
# MAGIC Harness the power of AI-driven data science workflows

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC In this demo, you'll learn to leverage Databricks' Data Science Agent to perform comprehensive exploratory data analysis and build machine learning models. The Data Science Agent transforms the Assistant into an intelligent companion that can automate entire multi-step data science workflows through natural language prompts.
# MAGIC
# MAGIC You'll work with real datasets to discover insights, create visualizations, and develop predictive models—all while learning how to effectively collaborate with AI to accelerate your data science projects. This lab demonstrates how modern AI tools can enhance productivity while maintaining data scientist oversight and control.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lab, you will be able to:
# MAGIC - Enable and configure the Data Science Agent in Databricks Assistant
# MAGIC - Use natural language prompts to perform exploratory data analysis on datasets
# MAGIC - Generate data visualizations and statistical summaries through AI assistance
# MAGIC - Build and evaluate machine learning models using the Data Science Agent
# MAGIC - Apply best practices for AI-assisted data science workflows

# COMMAND ----------

# MAGIC %md
# MAGIC ## Important: Select Environment 4
# MAGIC The cells below may not work in other environments. To choose environment 4: 
# MAGIC 1. Click the ![environment.png](../Includes/images/environment.png "environment.png") button on the right sidebar
# MAGIC 1. Open the **Environment version** dropdown
# MAGIC 1. Select **4**

# COMMAND ----------

# MAGIC %md
# MAGIC **Important:** The Data Science Agent can generate and execute code in your notebook. While it has guardrails to prevent dangerous actions, you should only use it with code and data you trust.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Enabling the Data Science Agent
# MAGIC
# MAGIC If you are not using Databricks Free Edition, enable the agent by following the directions under "Requirements" [here](https://docs.databricks.com/aws/en/notebooks/ds-agent#requirements)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Access the Data Science Agent
# MAGIC
# MAGIC To activate the Data Science Agent, you'll need to:
# MAGIC 1. Open the Assistant side panel in your notebook by clicking ![databricks_academy_logo.png](./Includes/images/assistant.png "assistant.png")
# MAGIC 2. Click the dropdown in the lower-right corner and select **Agent** (if it's not already selected) to toggle Agent mode
# MAGIC 3. Verify you can see the Agent interface is active

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Discovery and Initial Exploration
# MAGIC
# MAGIC The Data Science Agent excels at helping you discover and understand datasets through natural language queries. We'll start by exploring available data sources.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Discover Available Datasets
# MAGIC
# MAGIC Use the Data Science Agent to find suitable datasets for our analysis. Try this example prompt in the Agent interface:
# MAGIC
# MAGIC "Find a dataset that contains wine quality data"
# MAGIC
# MAGIC Note that the agent finds the wine quality table in the dbacademy.get_started_ml catalog/schema.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Initial Data Examination
# MAGIC
# MAGIC Now that you've identified a dataset, use the Data Science Agent to perform initial exploration. Paste this prompt in the Agent:
# MAGIC
# MAGIC ***Describe the @wine_quality_table dataset. Show me the schema, first few rows, and basic statistics about the data.***
# MAGIC
# MAGIC Now, place the cursor at the end of the words, ***@wine_quality_table***. Then, select the name of the table from the list that pops up above the prompt window and execute the prompt.
# MAGIC
# MAGIC If the Agent needs to execute code, it will ask for your approval.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Comprehensive Exploratory Data Analysis
# MAGIC
# MAGIC The Data Science Agent can perform sophisticated EDA tasks through natural language instructions. This section guides you through comprehensive data exploration.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Statistical Analysis and Data Profiling
# MAGIC
# MAGIC Use the Agent to generate comprehensive statistical summaries and identify data quality issues.
# MAGIC
# MAGIC Use the same process as above to execute the next prompt:
# MAGIC
# MAGIC ***Perform comprehensive EDA on @wine_quality_table. I want to understand column statistics, data distributions, missing values, and potential data quality issues. Think like a data scientist and provide insights.***
# MAGIC
# MAGIC The Agent may ask for your permission to execute code or cells that it generates. Grant this permission, as needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Visualization and Pattern Discovery
# MAGIC
# MAGIC Leverage the Agent's visualization capabilities to uncover patterns and relationships in your data.
# MAGIC
# MAGIC Use the same process as above to execute the next prompt:
# MAGIC
# MAGIC ***Generate correlation analysis and heatmaps to identify relationships between numeric columns***
# MAGIC
# MAGIC The Agent may ask for your permission to execute code or cells that it generates. Grant this permission, as needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Business Insights and Anomaly Detection
# MAGIC
# MAGIC Use the Agent to identify business-relevant insights and potential anomalies in the data.
# MAGIC
# MAGIC Use the same process as above to execute the next prompt:
# MAGIC
# MAGIC ***Analyze the data to identify business insights and any anomalies or outliers that need attention.***
# MAGIC
# MAGIC The Agent may ask for your permission to execute code or cells that it generates. Grant this permission, as needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Machine Learning Model Development
# MAGIC
# MAGIC Now we'll use the Data Science Agent to build and evaluate machine learning models based on our exploratory analysis.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Define the Machine Learning Problem
# MAGIC
# MAGIC Work with the Agent to identify appropriate machine learning use cases based on your data exploration.
# MAGIC
# MAGIC Use the same process as above to execute the next prompt:
# MAGIC
# MAGIC ***Which machine learning use cases would you recommend with this data?***
# MAGIC
# MAGIC The Agent may ask for your permission to execute code or cells that it generates. Grant this permission, as needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Preparation and Feature Engineering
# MAGIC
# MAGIC Use the Agent to prepare your data for machine learning, including feature engineering and data preprocessing.
# MAGIC
# MAGIC Use the same process as above to execute the next prompt:
# MAGIC
# MAGIC ***Identify which features most influence wine quality, guiding process improvements and ingredient selection.***
# MAGIC
# MAGIC The Agent may ask for your permission to execute code or cells that it generates. Grant this permission, as needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Model Training and Evaluation
# MAGIC
# MAGIC Leverage the Agent to build, train, and evaluate multiple machine learning models.

# COMMAND ----------

# MAGIC %md
# MAGIC Use the same process as above to execute the next prompt:
# MAGIC
# MAGIC ***Train multiple machine learning models on our prepared dataset to predict wine quality using the most important features. Compare different algorithms (e.g., Random Forest, Gradient Boosting, Linear models) and evaluate them using appropriate metrics. Show me model performance comparisons and feature importance.***
# MAGIC
# MAGIC The Agent may ask for your permission to execute code or cells that it generates. Grant this permission, as needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Model Optimization and Hyperparameter Tuning
# MAGIC
# MAGIC Use the Agent to optimize your best-performing model through hyperparameter tuning.
# MAGIC
# MAGIC Use the same process as above to execute the next prompt:
# MAGIC
# MAGIC ***Perform hyperparameter tuning on the best-performing model from our comparison. Use techniques like grid search or random search to optimize model performance. Show me the improvement in metrics after tuning.***
# MAGIC
# MAGIC The Agent may ask for your permission to execute code or cells that it generates. Grant this permission, as needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Model Interpretation and Business Insights
# MAGIC
# MAGIC The final step involves interpreting your machine learning results and extracting actionable business insights.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Feature Importance and Model Explainability
# MAGIC
# MAGIC Use the same process as above to execute the next prompt:
# MAGIC
# MAGIC ***Analyze the feature importance of our final model. Create visualizations showing which features are most predictive and explain what this means for the business. Use SHAP values or other explainability techniques if appropriate.***
# MAGIC
# MAGIC The Agent may ask for your permission to execute code or cells that it generates. Grant this permission, as needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Business Recommendations and Next Steps
# MAGIC
# MAGIC Use the same process as above to execute the next prompt:
# MAGIC
# MAGIC ***Based on our EDA and machine learning results, provide business recommendations and actionable insights. What should stakeholders know about the patterns we discovered? What are the next steps for deploying or improving this model?***
# MAGIC
# MAGIC The Agent may ask for your permission to execute code or cells that it generates. Grant this permission, as needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary and Reflection
# MAGIC
# MAGIC Congratulations! You've successfully completed a comprehensive data science workflow using the Databricks Data Science Agent.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Takeaways
# MAGIC
# MAGIC Reflect on your experience using the Data Science Agent:
# MAGIC
# MAGIC - **Efficiency Gains:** How did the Agent accelerate your data science workflow?
# MAGIC - **Code Quality:** What was the quality of the generated code and analysis?
# MAGIC - **Learning Experience:** What new techniques or insights did you discover?
# MAGIC - **Collaboration:** How effectively could you guide the Agent to achieve your objectives?

# COMMAND ----------

# MAGIC %md
# MAGIC ### Best Practices for AI-Assisted Data Science
# MAGIC
# MAGIC Based on this experience, consider these best practices:
# MAGIC
# MAGIC 1. **Clear Prompts:** Provide specific, context-rich prompts referencing datasets with @table_name
# MAGIC 2. **Iterative Refinement:** Use follow-up prompts to refine and improve results
# MAGIC 3. **Human Oversight:** Always review and validate Agent-generated code and insights
# MAGIC 4. **Domain Knowledge:** Combine AI capabilities with your domain expertise
# MAGIC 5. **Documentation:** Use the Agent to help document and explain complex analyses

# COMMAND ----------

# MAGIC %md
# MAGIC ### Next Steps
# MAGIC
# MAGIC Continue your AI-assisted data science journey:
# MAGIC
# MAGIC - Experiment with different datasets and use cases
# MAGIC - Explore advanced prompting techniques for specific domains
# MAGIC - Integrate Agent workflows into production data science processes
# MAGIC - Share insights and best practices with your team