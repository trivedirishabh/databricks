# Databricks notebook source
# MAGIC %md
# MAGIC ![databricks_academy_logo.png](./Includes/images/databricks_academy_logo.png "databricks_academy_logo.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # Tracking and Managing Models with MLflow
# MAGIC
# MAGIC In this demo, we will explore the model development lifecycle using MLflow. You’ll train a model, log artifacts, metrics, and parameters using MLflow, and then register the model in Unity Catalog for production readiness.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC - Train and log models using MLflow
# MAGIC - Track experiments and view runs using MLflow UI
# MAGIC - Register a model in Unity Catalog
# MAGIC - Use model version aliases like `staging` and `dev`

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
# MAGIC ## Part 1: Data Preparation for MLflow
# MAGIC
# MAGIC For this first part, we will read in a customer table, create a feature table, and register that feature table to Databricks Feature Store. This is all performed in the background and was covered in `01 - EDA and Feature Engineering`. Next, we will separate out our features from the target variable and perform a train-test split. 
# MAGIC
# MAGIC Note: We are working with a Pandas DataFrame called `training_df`.

# COMMAND ----------

# Load the feature table
training_df = spark.read.format('delta').table(f'{catalog_name}.{schema_name}.wine_quality_features').toPandas()

# COMMAND ----------

from sklearn.model_selection import train_test_split

# Define the mapping
mapping = {'Low': 0.0, 'Average': 1.0, 'High': 2.0}

# Apply the mapping to the 'pHCategory' column
training_df['pHCategory'] = training_df['pHCategory'].map(mapping)
# Use the training dataset to store variables X, the features, and y, the target variable. 
X = training_df.drop(columns = ["quality"])
y = training_df["quality"]



# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# COMMAND ----------

display(training_df)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Part 2: Training And Model Tracking/Management With MLflow
# MAGIC
# MAGIC Now that we have our training set ready to go, the next step is to train a model using the `sklearn` library. We will build a random forest classification model, tracking the F1-score for a single run. We will initiate the tracking before creating the model using `mlflow.start_run()` as the context manager. Within this manager we will:
# MAGIC
# MAGIC 1. Initialize the random forest classifier
# MAGIC 2. Fit the model
# MAGIC Make a prediction using our test set
# MAGIC 3. Log the F1-score metric as `test_f1`
# MAGIC 4. Capture the artifacts for model tracking and management using the flavor `mlflow.sklearn`. *Flavor* in this context simply means that MLflow will package our scikit-learn model in a consistent and standardized way. If we wished to use a different ML library, we would use a different *flavor*.
# MAGIC
# MAGIC Finally, we will register the model to Unity Catalog. Note, Databricks does not recommend registering your model at the Workspace level. Recall that we did this using the UI in the previous lab `02 - Experimentation with Mosaic AI AutoML`.
# MAGIC
# MAGIC

# COMMAND ----------

import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# set the path for mlflow experiment
mlflow.set_experiment(f"/Users/{username}/get-started-with-ml-flow-experiment")

with mlflow.start_run(run_name = 'get-started-with-ml-flow-run') as run:  
    # Initialize the Random Forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

    # Fit the model on the training data
    rf_classifier.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = rf_classifier.predict(X_test)

    # Enable automatic logging of input samples, metrics, parameters, and models
    mlflow.sklearn.autolog(
        log_input_examples = True,
        silent = True
    )
    # Calculate F1 score with 'macro' averaging for multiclass
    mlflow.log_metric("test_f1", f1_score(y_test, y_pred, average='macro'))
    # mlflow.log_metric("test_f1", f1_score(y_test, y_pred))
        
    mlflow.sklearn.log_model(
        rf_classifier,
        artifact_path = "model-artifacts", 
        input_example=X_train[:3],
        signature=infer_signature(X_train, y_train)
    )

    model_uri = f"runs:/{run.info.run_id}/model-artifacts"

# COMMAND ----------

# Modify the registry uri to point to Unity Catalog
mlflow.set_registry_uri("databricks-uc")

# Define the model name 
model_name = f"{catalog_name}.{schema_name}.my_model"

# Register the model in the model registry
registered_model = mlflow.register_model(model_uri=model_uri, name=model_name)

# COMMAND ----------

# MAGIC %md
# MAGIC Finally, we are going to add an alias for this version of the model. 

# COMMAND ----------

from mlflow.tracking.client import MlflowClient

# Initialize an MLflow Client
client = MlflowClient()

# Assign a "dev" alias to model version 1
client.set_registered_model_alias(
    name= registered_model.name,  # The registered model name
    alias="dev",  # The alias representing the dev environment
    version=registered_model.version  # The version of the model you want to move to "dev"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Navigate to your model in Catalog explorer, if desired.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prepare for the Next Demo
# MAGIC **We will discuss the code below in the next demo.**
# MAGIC
# MAGIC Run the next cell to deploy the model to Mosaic AI Model Serving. We will discuss this in the next demo of the course, but the deployment will take about 10-12 minutes, so we are deploying now to save some time.
# MAGIC
# MAGIC > **Please note**: Databricks Free Edition has caps on the number of model serving endpoints you can deploy. If you run into errors in any of the following cell, please double-check that you have not hit these caps.

# COMMAND ----------

from mlflow.deployments import get_deploy_client

client = get_deploy_client("databricks")
endpoint_name = f"{username}-model"
endpoint_name = endpoint_name.replace('.', '-').replace('@', '-')

# Check if the endpoint already exists
try:
    # Attempt to get the endpoint
    existing_endpoint = client.get_endpoint(endpoint_name)
    print(f"Endpoint '{endpoint_name}' already exists.")
except Exception as e:
    # If not found, create the endpoint
    if "RESOURCE_DOES_NOT_EXIST" in str(e):
        print(f"Creating a new endpoint: {endpoint_name}")
        endpoint = client.create_endpoint(
            name=endpoint_name,
            config={
                "served_entities": [
                    {
                        "name": "my-model",
                        "entity_name": registered_model.name,
                        "entity_version": registered_model.version,
                        "workload_size": "Small",
                        "scale_to_zero_enabled": True
                    }
                ],
                "traffic_config": {
                    "routes": [
                        {
                            "served_model_name": "my-model",
                            "traffic_percentage": 100
                        }
                    ]
                }
            }
        )
    else:
        print(f"An error occurred: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusions And Next Steps
# MAGIC
# MAGIC In this demo, we covered how to track, manage, and stage models using **MLflow** on Databricks. In the next notebook, you'll explore **Mosaic AI AutoML**, which abstracts many of these steps into a no-code/low-code UI-driven workflow. This will help you compare the manual MLflow approach with the AutoML pipeline, and understand how MLflow operates under the hood of AutoML.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>