During Implementation...
# Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis
## Project Overview
This project automates an Data pipeline using Python. Data is first profiled (reviewed and cleansed) before being loaded into Cloud SQL. Cloud Composer, managing Apache Airflow on GCP, orchestrates the pipeline to transform the data from Cloud SQL and load it into BigQuery. Finally, Looker Studio visualizes the data.
## About Dataset
The dataset contains real-world complaints about financial products and services, with attributes such as product type, issue description, company response, and metadata. This diverse complaints data is the input source for the ETL pipeline and data visualization.
## Architecture
![image](https://github.com/getnkit/Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis/blob/1aae4c7285eaed59480fda3a933bd6ad14cd1346/images/Data%20Architecture.png
## Implementation
### Step 1: Data profiling using Python on Google Colab\
### Step 2: Import profiled data into Cloud SQL(MySQL) using Python script\
- **Imports necessary modules:** Uses configparser for reading configuration files and pandas for data manipulation.
- **Specifies the configuration file path:** Defines the path to the configuration file containing database connection details.
- **Parses the configuration file:** Reads the configuration file to extract database connection parameters.
- **Retrieves database connection details:** Extracts the database name, username, password, host, and port from the configuration file.
- **Constructs the database URI:** Builds the connection URI for the MySQL database using the retrieved details.
- **Reads data from CSV files:** Loads data into Pandas DataFrames.
- **Imports data into the MySQL database:** Writes the DataFrames to the corresponding tables in the MySQL database, replacing the existing data if the tables already exist.
### Step 3: Preparation to create bucket on Google Cloud Storage (GCS) and dataset on BigQuery\
### Step 4: Implementing Python DAG in Airflow\
**Step 4.1:** Importing Modules
- To import necessary modules and libraries for the DAG.

**Step 4.2:** Extract Data from MySQL
- Connects to a MySQL database using MySqlHook.
- Fetches data from two tables and loads them into Pandas DataFrames.
- Saves these DataFrames as CSV files in the specified directory.

**Step 4.3:** Transform Data
- Connects to a MySQL database using MySqlHook.
- Reads the previously saved CSV files into Pandas DataFrames.
- Converts necessary columns to string type to ensure proper merging.
- Merges the two DataFrames based on the state code and abbreviation.
- Drops redundant columns and rearranges the columns.
- Saves the transformed DataFrame as a CSV file in the specified directory.

**Step 4.4:** Load Data to Google Cloud Storage (GCS)
- Prepares Google Cloud Storage credentials from Airflow Variables.
- Initializes a Google Cloud Storage client using the credentials.
- Specifies the bucket name and file path for uploading the transformed CSV file.
- Uploads the file to the specified GCS bucket and path.

**Step 4.5:** Load Data from GCS to BigQuery
- Prepares Google BigQuery credentials from Airflow Variables.
- Initializes a BigQuery client using the credentials.
- Specifies the BigQuery table ID and job configuration for loading the CSV file from GCS.
- Loads the CSV file from GCS to the specified BigQuery table, using the configured job settings (e.g., skipping the first row, auto-detecting schema, etc.).

**Step 4.6:** Airflow DAG Definition
- Defines the DAG name.
- Sets the start date to one day ago and schedules the DAG to run once (@once).
- Tags the DAG with "financial", "mysql", and "bigquery".

### Step 5: Trigger Python DAG to automated ETL data pipeline\
### Step 6: Developed Consumer Financial Complaints Dashboard using Looker Studio with BigQuery plug-in.


