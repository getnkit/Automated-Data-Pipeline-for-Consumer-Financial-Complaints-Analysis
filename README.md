During Implementation...
# Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis
## Project Overview
This project focuses on building and automating a Python ETL pipeline with Airflow. Before ingesting data into the automated data pipeline, it undergoes Data Profiling (review and cleansing) and is then uploaded to Cloud SQL (MySQL) using a Python script. Subsequently, the automated data pipeline extracts data from MySQL, transforms the data, and loads it into Google Cloud Storage (GCS) to ingest the data into BigQuery. Finally, a Consumer Financial Complaints Dashboard is developed using Looker Studio.
## About Dataset
This dataset consists of real-world complaints about financial products and services, including details such as product type, issue description, company response, and other metadata. These complaints are published after the company responds, or after 15 days from the date of receipt, whichever comes first. By voicing their opinions and complaints, consumers help improve the quality and efficiency of the financial marketplace.
## Architecture
![image](https://github.com/getnkit/Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis/blob/6b4f65c2430bc17d4b98fd647810c5b0b4847f9a/images/Data%20Architecture.png)
## Implementation
### Step 1: Data profiling using Python on Google Colab
### Step 2: Import profiled data into Cloud SQL(MySQL) using Python script
- **Imports necessary modules:** Uses configparser for reading configuration files and pandas for data manipulation.
- **Specifies the configuration file path:** Defines the path to the configuration file containing database connection details.
- **Parses the configuration file:** Reads the configuration file to extract database connection parameters.
- **Retrieves database connection details:** Extracts the database name, username, password, host, and port from the configuration file.
- **Constructs the database URI:** Builds the connection URI for the MySQL database using the retrieved details.
- **Reads data from CSV files:** Loads data into Pandas DataFrames.
- **Imports data into the MySQL database:** Writes the DataFrames to the corresponding tables in the MySQL database, replacing the existing data if the tables already exist.
### Step 3: Create a bucket on Google Cloud Storage (GCS) and a dataset on BigQuery for ETL pipeline
### Step 4: Create Python DAG in Airflow
**Step 4.1:** Importing Modules
- Import necessary modules and libraries for the DAG.

**Step 4.2:** Extract Data from MySQL
- Connects to a MySQL database using MySqlHook.
- Fetches data from two tables and loads them into Pandas DataFrames.
- Saves these DataFrames as CSV files in the specified directory.

**Step 4.3:** Transform Data
- Reads the previously saved CSV files into Pandas DataFrames.
- Converts necessary columns to string type to ensure proper merging.
- Merges the two DataFrames.
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
- Create task specifies an individual step in a workflow.
- Set up dependencies or the order in which tasks should be executed.

### Step 5: Run DAG files in Airflow Webserver, which runs on Docker
![image](https://github.com/getnkit/Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis/blob/40443b93862cb87771b83e513496b4bab184abfa/images/ETL%20Pipeline%20with%20Airflow.png)
### Step 6: Developed Consumer Financial Complaints Dashboard using Looker Studio connected to a Google BigQuery table


