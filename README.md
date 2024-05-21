During Implementation...
# Automated-Data-Pipeline-for-Consumer-Financial-Complaints-Analysis
## Project Overview
This project automates an Data pipeline using Python. Data is first profiled (reviewed and cleansed) before being loaded into Cloud SQL. Cloud Composer, managing Apache Airflow on GCP, orchestrates the pipeline to transform the data from Cloud SQL and load it into BigQuery. Finally, Looker Studio visualizes the data.
## About Dataset
The dataset contains real-world complaints about financial products and services, with attributes such as product type, issue description, company response, and metadata. This diverse complaints data is the input source for the ETL pipeline and data visualization.
## Architecture
![image](https://github.com/getnkit/Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis/blob/1aae4c7285eaed59480fda3a933bd6ad14cd1346/images/Data%20Architecture.png
## Implementation
**Step 1:** Data profiling with Python using Google Colab\
**Step 2:** Import profiled data into Cloud SQL(MySQL) using Python script\
**Step 3:** Create a database on Cloud SQL and move data from Google Storage to dataset tables\
\
![image](https://github.com/getnkit/Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis/blob/3b3164c16dffff0fc610b350650dd795cee9de06/images/Sample%20Table.png)\
\
**Step 4:** Create Cloud Composer environment\
**Step 5:** Create a table within a dataset on BigQuery\
**Step 6:** Run Python script to automated ETL pipeline\
**Step 7:** Query data on BigQuery\
**Step 8:** Create dashboard to gain insight


