# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img
# MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
# MAGIC     alt="Databricks Learning"
# MAGIC   >
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # 08.Lab - Getting Started with Databricks for Machine Learning
# MAGIC
# MAGIC In this lab, we will construct a comprehensive ML model pipeline using Databricks. Initially, we will train and monitor our model using mlflow. Subsequently, we will register the model and advance it to the next stage. In the latter part of the lab, we will utilize Model Serving to deploy the registered model. Following deployment, we will interact with the model via a REST endpoint and examine its behavior through an integrated monitoring dashboard.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Important: Select Environment 4
# MAGIC The cells below may not work in other environments. To choose environment 4: 
# MAGIC 1. Click the ![environment.png](../Includes/images/environment.png "environment.png") button on the right sidebar
# MAGIC 1. Open the **Environment version** dropdown
# MAGIC 1. Select **4**

# COMMAND ----------

# MAGIC %md
# MAGIC ## Install Necessary Python Libraries
# MAGIC Run the next cell to install python libraries.

# COMMAND ----------

!pip install databricks-feature-engineering
%restart_python

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Requirements
# MAGIC Ensure you have completed all tasks in the notebook, [Performing EDA and Feature Engineering]($./03 - Performing EDA and Feature Engineering)
# MAGIC
# MAGIC The next cell will create some python variables that will be used in the notebook.

# COMMAND ----------

####################################################################################
# Set python variables for catalog and schema
catalog_name = "dbacademy"
schema_name = "get_started_ml"
# Capture username
username = dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
####################################################################################

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import Sample Data
# MAGIC We are going to use a sample dataset that is available in the Databricks Marketplace. To import the sample data, perform the following actions:
# MAGIC
# MAGIC 1. In the left navigation bar, right-click **Marketplace**, and select **Open Link in New Tab**.
# MAGIC
# MAGIC 2. In this new tab, paste the following into the search bar marked "Search for products" (not the search bar at the top of the window): **Airbnb Sample Data**
# MAGIC
# MAGIC 3. Click the card named **Airbnb Sample Data**
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
# MAGIC - **Catalog name**: databricks_airbnb_sample_data 
# MAGIC  
# MAGIC - **Schema name**: v01
# MAGIC
# MAGIC - **Volume name**: sf-listings
# MAGIC
# MAGIC We will use this data throughout the lesson.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Data Ingestion
# MAGIC
# MAGIC Airbnb Sample Data
# MAGIC
# MAGIC  The first step in this lab is to ingest data from .csv files and save them as delta tables. 
# MAGIC  
# MAGIC  - Find `airbnb-cleaned-mlflow.csv` located in the volume `sf-listings`. 
# MAGIC  - Replace `<FILL_IN>` with the full path to this CSV file in the cell below.
# MAGIC
# MAGIC  > Note: if you need help, the cell immediately following the cell below contains the solution.

# COMMAND ----------

## Copy and paste the location of the airbnb dataset
file_path = '<FILL_IN>'

# COMMAND ----------

# MAGIC %skip
# MAGIC file_path = '/Volumes/databricks_airbnb_sample_data/v01/sf-listings/airbnb-cleaned-mlflow.csv'

# COMMAND ----------

## Read in the csv file and store it in Unity Catalog within the catalog and schema shown in cell 7. 
## Name your delta table "airbnb_lab"
my_table = <FILL_IN>
df = spark.read.format(<FILL_IN>).option("header", "true").load(<FILL_IN>)

# COMMAND ----------

# MAGIC %skip
# MAGIC my_table = "airbnb_lab"
# MAGIC df = spark.read.format("csv").option("header", "true").load(file_path)
# MAGIC
# MAGIC display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC Let's preprocess this dataset since the schema shows all variables being of time `string`.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import FloatType, IntegerType, StringType

## Specify columns that should be treated as categorical (e.g., integers in categorical context)
categorical_columns = ['neighbourhood_cleansed', 'zipcode', 'property_type', 'room_type', 'bed_type']
for col in categorical_columns:
    df = df.withColumn(col, df[col].cast(StringType()))

## Specify columns that should remain as floats for machine learning
numerical_columns = ['host_total_listings_count', 'latitude', 'longitude', 'accommodates', 'bathrooms', 
                 'bedrooms', 'beds', 'minimum_nights', 'number_of_reviews', 'review_scores_rating',
                 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin',
                 'review_scores_communication', 'review_scores_location', 'review_scores_value', 'price']
for col in numerical_columns:
    df = df.withColumn(col, df[col].cast(FloatType()))

df = df.withColumn("airbnb_id", F.monotonically_increasing_id()).select(['airbnb_id'] + numerical_columns + categorical_columns)

## Check the schema to confirm data type changes
df.printSchema()

# COMMAND ----------

df.write.format('delta').mode('overwrite').saveAsTable(f'{catalog_name}.{schema_name}.airbnb_lab')

# COMMAND ----------

# MAGIC %md
# MAGIC # Feature Engineering

# COMMAND ----------

# MAGIC %md
# MAGIC Next, using PySpark, create a DataFrame called `feature_df` that is the feature table. Recall that the feature table must contain a primary key and does not contain the target variable, which is `price` in our case.

# COMMAND ----------

feature_df = df.select(<FILL_IN>)

## Find rooms with a score of at least 6.0 and 80 reviews
feature_df = feature_df.filter((<FILL_IN>) & (<FILL_IN>))
display(feature_df)

# COMMAND ----------

# MAGIC %skip
# MAGIC feature_df = df.select(['airbnb_id'] + numerical_columns)
# MAGIC
# MAGIC ## Find rooms with a score of at least 6.0 and 80 reviews
# MAGIC feature_df = feature_df.filter((df.review_scores_rating >= 6.0) & (df.number_of_reviews >= 80))
# MAGIC display(feature_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Write to Databricks Feature Store. Remember, we do not include our target variable.

# COMMAND ----------

## Write feature_df to Databricks Feature Store. 
from databricks.feature_engineering import FeatureEngineeringClient

fs = FeatureEngineeringClient()

feature_df = feature_df.drop(<FILL_IN>)

fs.create_table(
    name=f"{catalog_name}.{schema_name}.airbnb_features",
    primary_keys = <FILL_IN>, 
    df = <FILL_IN>,
    description = "This is the airbnb feature table",
    tags = {"source": "bronze", "format": "delta"}
    )

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Write feature_df to Databricks Feature Store.
# MAGIC from databricks.feature_engineering import FeatureEngineeringClient
# MAGIC
# MAGIC fs = FeatureEngineeringClient()
# MAGIC
# MAGIC feature_df = feature_df.drop("price")
# MAGIC
# MAGIC fs.create_table(
# MAGIC     name=f"{catalog_name}.{schema_name}.airbnb_features",
# MAGIC     primary_keys = ['airbnb_id'], 
# MAGIC     df = feature_df,
# MAGIC     description = "This is the airbnb feature table",
# MAGIC     tags = {"source": "bronze", "format": "delta"}
# MAGIC     )

# COMMAND ----------

# MAGIC %md
# MAGIC # Train a Model
# MAGIC To summarize what you have accomplished so far:
# MAGIC 1. You have created a table that is a snapshot of the original dataset (Airbnb csv file) called `airbnb_lab`.
# MAGIC 1. You have created a feature table and stored it in Databricks Feature Store called `airbnb_features`.
# MAGIC
# MAGIC Next, we will simulate the process of reading in these Delta tables and training a model. We will train a machine learning model and register it to Unity Catalog.

# COMMAND ----------

from sklearn.model_selection import train_test_split
## Read in the feature table airbnb_features from Unity Catalog using PySpark and store it as training_df
prediction_df = spark.read.format('delta').table(f'{catalog_name}.{schema_name}.<FILL_IN>').select(<FILL_IN>)
features_df = spark.read.format('delta').table(f'{catalog_name}.{schema_name}.<FILL_IN>')  

## Join these two dataframes on airbnb_id
training_df = prediction_df.join(<FILL_IN>, on='airbnb_id').toPandas()

## Perform train-test split
X = training_df.drop(columns = [<FILL_IN>])
y = training_df[<FILL_IN>]

X_train, X_test, y_train, y_test = train_test_split(<FILL_IN>, <FILL_IN>, test_size=0.2, random_state=42)

# COMMAND ----------

# MAGIC %skip
# MAGIC from sklearn.model_selection import train_test_split
# MAGIC ## Read in the feature table airbnb_features from Unity Catalog using PySpark and store it as training_df
# MAGIC prediction_df = spark.read.format('delta').table(f'{catalog_name}.{schema_name}.airbnb_lab').select('airbnb_id','price')
# MAGIC features_df = spark.read.format('delta').table(f'{catalog_name}.{schema_name}.airbnb_features')
# MAGIC
# MAGIC ## Join these two dataframes on airbnb_id
# MAGIC training_df = prediction_df.join(features_df, on='airbnb_id').drop('airbnb_id')
# MAGIC training_pdf = training_df.toPandas()
# MAGIC
# MAGIC ## Perform train-test split
# MAGIC X = training_pdf.drop(columns = ['price'])
# MAGIC y = training_pdf['price']
# MAGIC
# MAGIC X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Model Tracking and Management with MLflow
# MAGIC
# MAGIC Next, you will use MLflow to track the training of your model.

# COMMAND ----------

import mlflow
## Set the path for mlflow experiment
mlflow.set_experiment(f"/Users/{username}/<FILL_IN>")

# COMMAND ----------

# MAGIC %skip
# MAGIC import mlflow
# MAGIC ## Set the path for mlflow experiment
# MAGIC mlflow.set_experiment(f"/Users/{username}/model-serving-experiment")

# COMMAND ----------

## Start the MLflow run
with mlflow.start_run(run_name=<FILL_IN>) as run:
    ## Initialize the Random Forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=<FILL_IN>, random_state=42)

    ## Fit the model on the training data
    rf_classifier.fit(<FILL_IN>, <FILL_IN>)

    ## Make predictions on the test data
    y_pred = rf_classifier.predict(<FILL_IN>)

    ## Enable automatic logging of input samples, metrics, parameters, and models
    mlflow.sklearn.autolog(log_input_examples=<FILL_IN>, silent=True)
    ## Calculate F1 score with 'macro' averaging for multiclass
    mlflow.log_metric("test_f1", f1_score(<FILL_IN>, <FILL_IN>, average="macro"))
    ## mlflow.log_metric("test_f1", f1_score(y_test, y_pred))

    mlflow.sklearn.log_model(
        rf_classifier,
        artifact_path="model-artifacts",
        input_example=X_train[:3],
        signature=infer_signature(<FILL_IN>, <FILL_IN>),
    )

    model_uri = f"runs:/{run.info.run_id}/model-artifacts"

# COMMAND ----------

# MAGIC %skip
# MAGIC from sklearn.ensemble import RandomForestClassifier
# MAGIC from sklearn.metrics import f1_score
# MAGIC from mlflow.models.signature import infer_signature
# MAGIC ## Start the MLflow run
# MAGIC with mlflow.start_run(run_name="model-serving-run") as run:
# MAGIC     ## Initialize the Random Forest classifier
# MAGIC     rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
# MAGIC
# MAGIC     ## Fit the model on the training data
# MAGIC     rf_classifier.fit(X_train, y_train)
# MAGIC
# MAGIC     ## Make predictions on the test data
# MAGIC     y_pred = rf_classifier.predict(X_test)
# MAGIC
# MAGIC     ## Enable automatic logging of input samples, metrics, parameters, and models
# MAGIC     mlflow.sklearn.autolog(log_input_examples=True, silent=True)
# MAGIC     ## Calculate F1 score with 'macro' averaging for multiclass
# MAGIC     mlflow.log_metric("test_f1", f1_score(y_test, y_pred, average="macro"))
# MAGIC     ## mlflow.log_metric("test_f1", f1_score(y_test, y_pred))
# MAGIC
# MAGIC     mlflow.sklearn.log_model(
# MAGIC         rf_classifier,
# MAGIC         artifact_path="model-artifacts",
# MAGIC         input_example=X_train[:3],
# MAGIC         signature=infer_signature(X_train, y_train),
# MAGIC     )
# MAGIC
# MAGIC     model_uri = f"runs:/{run.info.run_id}/model-artifacts"

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Register the Model
# MAGIC
# MAGIC Now, let's register the trained model in the model registry:
# MAGIC
# MAGIC 1. Use the logged model from the previous step.
# MAGIC 2. Provide a name and description for the model.
# MAGIC 3. Register the model to Unity Catalog.

# COMMAND ----------

## Modify the registry uri to point to Unity Catalog
mlflow.set_registry_uri("databricks-uc")

sanitized_username = username.replace('.', '-').replace('@', '-')
model_name = f"gs_db_ml_LAB_{sanitized_username}"

## Register the model in the model registry
registered_model = mlflow.register_model(model_uri=model_uri, name=f'{catalog_name}.{schema_name}.{model_name}')

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Manage Model Stages
# MAGIC
# MAGIC As the model is registered into Model Registry, we can manage its stage using the UI or the API. In this demo, we will use the API to transition registered model to `Staging` stage.

# COMMAND ----------

from mlflow.tracking.client import MlflowClient
client = MlflowClient()

## Transition the model to the "lab-staging" stage
client.<FILL_IN>(
    name = <FILL_IN>,
    version = <FILL_IN>,
    stage = <FILL_IN>
)

# COMMAND ----------

# MAGIC %skip
# MAGIC from mlflow.tracking.client import MlflowClient
# MAGIC
# MAGIC ## Initialize an MLflow Client
# MAGIC client = MlflowClient()
# MAGIC
# MAGIC ## Assign a "staging" alias to model version 1
# MAGIC client.set_registered_model_alias(
# MAGIC     name= registered_model.name,  # The registered model name
# MAGIC     alias="lab-staging",  # The alias representing the staging environment
# MAGIC     version=registered_model.version  # The version of the model you want to move to "staging"
# MAGIC )

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Part 3: Mosaic AI Model Serving
# MAGIC
# MAGIC **Setting Up Model Serving**
# MAGIC
# MAGIC We can create Model Serving endpoints with the Databricks Machine Learning API or the Databricks Machine Learning UI. An endpoint can serve any registered Python MLflow model in the **Model Registry**.
# MAGIC
# MAGIC In order to keep it simple, in this lab, we are going to use the Model Serving UI for creating, managing and using the Model Serving endpoints. We can create model serving endpoints with the **"Serving"** page UI or directly from registered **"Models"** page.  
# MAGIC
# MAGIC Let's go through the steps of creating a model serving endpoint in Models page.
# MAGIC
# MAGIC - In the left navigation bar, right-click **Models** and select "Open Link in New Tab". 
# MAGIC
# MAGIC - Select **Owned by me**.
# MAGIC
# MAGIC - Select the model you want to serve under the **Name** column (the model we created earlier is called "gs_db_ml_LAB_your-username"). This will take you to the Catalog Explorer. 
# MAGIC
# MAGIC - Click **Serve this model** in the top-right corner. This will take you to the **Serving endpoints** screen.
# MAGIC
# MAGIC - In **General**, enter a name for the endpoint. Note that this name is used in the URL for the endpoint.
# MAGIC
# MAGIC - There are several configurations under **Served entities** that we will not discuss here. Leave **Entity**, **Compute type** and **Compute scale-out** to default values. If you are using Databricks Free Edition, ensure **Scale to zero** is selected.
# MAGIC
# MAGIC - Click **Create** in the lower-right corner. 
# MAGIC
# MAGIC The endpoint will take about 12 minutes to provision.
# MAGIC
# MAGIC >Please note: Databricks Free Edition places caps on the number of serving endpoints you can provision. If you are unable to provision an endpoint, please verify that you have not hit this cap in your environment.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query Serving Endpoint
# MAGIC
# MAGIC Let's use the deployed model for real-time inference. Here’s a step-by-step guide for querying an endpoint in Databricks Model Serving:
# MAGIC
# MAGIC - Go to the **Serving** endpoints page and select the endpoint you want to query.
# MAGIC
# MAGIC - Click **Use** button the top right corner.
# MAGIC
# MAGIC - There are 4 methods for querying an endpoint; **browser**, **CURL**, **Python**, and **SQL**. For now, let's use the easiest method; querying right in the **browser** window. In this method, we need to provide the input parameters in JSON format. Recall that we registered an example with MLflow, which appears automatically when selecting **browser**.
# MAGIC
# MAGIC - Click **Send request**.
# MAGIC
# MAGIC - **Response** field on the right panel will show the result of the inference.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lab, we explored the full potential of the Databricks Data Intelligence Platform for machine learning tasks. From data ingestion to model deployment, we covered essential steps such as data preparation, model training, tracking, registration, and serving. By utilizing MLflow for model tracking and management, and Model Serving for deployment, we demonstrated how Databricks offers a seamless experience.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>