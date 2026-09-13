# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Performing EDA and Feature Engineering
# MAGIC
# MAGIC In this lesson, we’ll walk you through basic exploratory data analysis and the process of creating and storing a feature table in the Feature Store. We’ll begin by demonstrating how to load data into a Spark DataFrame, view essential statistical information, and perform visual analysis using both built-in tools and code. Next, we’ll create a feature table, showing you how to store and explore it within the Feature Store UI. By the end of this demo, you should have a foundational understanding of the key steps involved in creating a feature table for Feature Engineering.
# MAGIC
# MAGIC ## **Learning Objectives**:
# MAGIC
# MAGIC _By the end of this demo, you will be able to:_
# MAGIC
# MAGIC
# MAGIC 1. **Perform Basic Exploratory Data Analysis (EDA):**
# MAGIC     - Utilize Spark and Pandas to store our data as a DataFrame.
# MAGIC     - Use built-in functionality to analyze data from a statistical perspective. Additionally, we will visualize the summary statistics. 
# MAGIC
# MAGIC
# MAGIC 2. **Introduction to Feature Engineering with Databricks:**
# MAGIC     - Create a feature table and store it in Feature Store from a PySpark DataFrame.
# MAGIC     - Inspect the Feature Store table using the UI and from the notebook.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Important: Select Environment 4
# MAGIC The cells below may not work in other environments. To choose environment 4: 
# MAGIC 1. Click the ![environment.png](../Includes/images/environment.png "environment.png") button on the right sidebar
# MAGIC 1. Open the **Environment version** dropdown
# MAGIC 1. Select **4**

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Requirements
# MAGIC
# MAGIC Please complete the following requirements before starting the lesson.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Install Necessary Python Libraries
# MAGIC Run the next cell to install python libraries.

# COMMAND ----------

!pip install databricks-feature-engineering
%restart_python

# COMMAND ----------

# MAGIC %md
# MAGIC ## Importing Sample Data
# MAGIC We are going to use a sample dataset that is available in the Databricks Marketplace. To import the sample data, perform the following actions:
# MAGIC
# MAGIC 1. In the left navigation bar, right-click **Marketplace**, and select **Open Link in New Tab**.
# MAGIC
# MAGIC 2. In this new tab, paste the following into the search bar marked "Search for products" (not the search bar at the top of the window): **Wine Quality Data**
# MAGIC
# MAGIC 3. Click the card named **Wine Quality Data**
# MAGIC
# MAGIC This data is available for you free of charge, but you must comply with the **Terms of Service** (link in the bottom-right of the screen)
# MAGIC
# MAGIC 4. In the upper-right corner, click **Get instant access**
# MAGIC
# MAGIC 5. As desired, read the various links. Then, click check the box, and click **Get instant access**
# MAGIC
# MAGIC 6. Click **Open** in the upper-right corner of the screen
# MAGIC
# MAGIC A new browser tab is launched, and you are taken to the Catalog Explorer. Note that the data is available to you under **Delta Shares Received**:
# MAGIC
# MAGIC - **Catalog name**: databricks_wine_quality_data 
# MAGIC  
# MAGIC - **Schema name**: v01
# MAGIC
# MAGIC We will use this data throughout these lessons.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC We first need to build some data assets and define some configuration variables required for this demonstration. 

# COMMAND ----------

from pyspark.sql import functions as F
####################################################################################
# Set python variables for catalog, schema, and volume names (change, if desired)
catalog_name = "dbacademy"
schema_name = "get_started_ml"
table_name = "wine_quality_table"
####################################################################################

####################################################################################
# Create the catalog and schema if they don't exist already
spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog_name}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}")
####################################################################################

####################################################################################
# Create a demo table
full_table_name = f"{catalog_name}.{schema_name}.{table_name}"

# Drop the table if it exists
if spark.catalog.tableExists(full_table_name):
    spark.sql(f"DROP TABLE {full_table_name}")

data_path = f"/Volumes/databricks_wine_quality_data/v01/data"

df = (
    spark.read.format("delta")
    .load(data_path)
    .withColumn("wine_id", F.monotonically_increasing_id())
    .select(
        "wine_id",
        "fixed_acidity",
        "volatile_acidity",
        "citric_acid",
        "residual_sugar",
        "chlorides",
        "free_sulfur_dioxide",
        "total_sulfur_dioxide",
        "density",
        "pH",
        "sulphates",
        "alcohol",
        "quality",
    )
)

df.write.format("delta").mode("overwrite").saveAsTable(full_table_name)
####################################################################################

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: Perform Basic Exploratory Data Analysis (EDA)
# MAGIC
# MAGIC In this section, we will show how you can utilize Databricks Notebooks for exploratory analysis. This will be presented in two flavors: built-in tools and demonstrative custom code.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Read and Inspect the Dataset
# MAGIC
# MAGIC In this section, we will utilize a fictional dataset from a wine rating company, which includes various information from acidity to pH levels. Ideally, a data scientist or machine learning practitioner, would take this dataset and perform various feature engineering tasks in order to be able to predict the `quality` rating of the wine. 
# MAGIC
# MAGIC The next cell will create one table: `wine_quality_table`. Let's create two different dataframes, one using Spark and another using pandas.  
# MAGIC

# COMMAND ----------

df = spark.read.table(f'{catalog_name}.{schema_name}.wine_quality_table')
pdf = df.toPandas()

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Inspect Statistics: Numerical Values and Visuals
# MAGIC
# MAGIC Here we will exhibit different ways in which you can display and visualize descriptive statistics. 
# MAGIC 1. `describe(<spark_or_pandas_dataframe>)` - This method will only return a table with the necessary information. You can recover the generated profile like that in the dbutils approach by adding a data profile. 
# MAGIC     - Click on the **+** icon and select **data profile**. 
# MAGIC 2. `display(<spark_or_pandas_dataframe>)` - This will return the table. From this, we can build a visual to inspect the feature variables. 
# MAGIC 3. Custom code - We can use the Pandas Dataframe along with other Python libraries to build custom visualizations.

# COMMAND ----------

display(df.describe())

# COMMAND ----------

print(pdf.describe())

# COMMAND ----------

display(df)

# COMMAND ----------

from pyspark.sql import functions as F

# Let's find Q1, median, and Q3 of pH grouped by the quality ranking for 

column_stats = 'pH'

display(df.groupBy('quality').agg(
    F.min(f'{column_stats}').alias('min'),
    F.expr(f'percentile({column_stats}, 0.25)').alias('Q1'),
    F.expr(f'percentile({column_stats}, 0.5)').alias('median'),
    F.expr(f'percentile({column_stats}, 0.75)').alias('Q3'),
    F.max(f'{column_stats}').alias('max')
))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Bubble Chart Using GUI Visualization Editor
# MAGIC
# MAGIC We can now use the **Visualization Editor** in the Databricks UI to build a bubble chart using our grouped summary statistics.

# COMMAND ----------

# MAGIC %md
# MAGIC **Steps:**
# MAGIC 1. Create the grouped DataFrame in the following cell.
# MAGIC 2. In the output result cell:
# MAGIC    - Click the **+**  dropdown next to Table (top-right of the table display).
# MAGIC    - Select **Visualization**.
# MAGIC
# MAGIC 3. In the **Visualization Editor**:
# MAGIC    - Select **Bubble** as the visualization type.
# MAGIC    - Under **X column**, select `quality`.
# MAGIC    - Under **Y columns**, select `median_pH`.
# MAGIC    - Under **Group by**, select `count`,
# MAGIC    - Under **Bubble size column**, select `count`.
# MAGIC    - Under **Bubble size coefficient**, check if it's `1`,
# MAGIC    - Leave **Bubble size proportional to** as `Diameter`.
# MAGIC
# MAGIC 4. Click **Save** to render the chart.
# MAGIC
# MAGIC This creates a bubble chart that shows:
# MAGIC - Wine **quality** on the x-axis.
# MAGIC - **Median pH** level on the y-axis.
# MAGIC - **Bubble size** proportional to the number of samples.
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import expr, count

grouped_df = df.groupBy("quality").agg(expr("percentile(pH, 0.5)").alias("median_pH"), count("pH").alias("count"))
display(grouped_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: Introduction to Feature Engineering on Databricks
# MAGIC
# MAGIC After exploring our data for a bit, we see that it would be beneficial to be able to predict `quality`. There are many things we can do to this dataset, such as outlier analysis, etc. Instead, since this is just an introductory lesson, let's keep it simple and add an additional feature that separates out low, average, and high `pH`. This will add an additional feature to the data we already have. 
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Business Logic
# MAGIC
# MAGIC Based on our analysis above, suppose business stakeholders give you the following guidelines for pH levels.
# MAGIC
# MAGIC 1. Low pH: <= Q1
# MAGIC 2. Average pH: < Q1 and < Q3
# MAGIC 3. High pH: >= Q3
# MAGIC
# MAGIC Let's take this business logic and create a new **feature** and store it in a feature table in our Feature Store.

# COMMAND ----------

feature_variables = ['fixed_acidity',
                     'volatile_acidity',
                     'citric_acid',
                     'pH',
                     'sulphates',
                     'alcohol',
                     'quality']
prediction_variable = 'quality'
primary_key = ['wine_id']

# COMMAND ----------

feature_df = df.select(primary_key + feature_variables)
display(feature_df)

# COMMAND ----------

from pyspark.sql.functions import col, expr, when

quantiles = feature_df.approxQuantile("pH", [0.25, 0.75], 0.0)

Q1, Q3 = quantiles

feature_df2 = feature_df.withColumn(
    "pHCategory",
    when(col("pH") <= Q1, "Low")
    .when((col("pH") > Q1) & (col("pH") < Q3), "Average")
    .otherwise("High")
)

display(feature_df2)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Save features to feature table
# MAGIC
# MAGIC Now that we have our feature store created, let's store it as a feature table within Feature Store. We have all the ingredients we need to do this within Databricks Unity Catalog: 
# MAGIC 1. Feature table (Spark DataFrame)
# MAGIC 2. Primary key (designated feature)

# COMMAND ----------

from databricks.feature_engineering import FeatureEngineeringClient

# Instantiate the FeatureEngineeringClient
fe = FeatureEngineeringClient()

# COMMAND ----------

# Set the feature table name for storage in UC
feature_table_name = f'{catalog_name}.{schema_name}.wine_quality_features'

print(f"The name of the feature table: {feature_table_name}\n\n")

# Create the feature table
fe.create_table(
    name = feature_table_name,
    primary_keys = primary_key,
    df = feature_df2, 
    description="Wine quality features", 
    tags = {"source": "bronze", "format": "delta"}
)

# COMMAND ----------

# MAGIC %md
# MAGIC Now, go inspect your feature table using the UI!

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusion And Next Steps
# MAGIC
# MAGIC In this lesson, we learned about basic EDA and how to perform feature engineering and save the result to our feature store. Notice that all a feature table is a Delta table that has a primary key. However, Features allows us to separate out those tables that will be used for ML versus those that will not.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>