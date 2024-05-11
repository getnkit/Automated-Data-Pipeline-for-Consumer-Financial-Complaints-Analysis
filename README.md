# Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis
## Project Overview
This project automates an ETL pipeline using Python. Data is first profiled (reviewed and cleansed) before being loaded into Cloud SQL. Cloud Composer, managing Apache Airflow on GCP, orchestrates the pipeline to transform the data from Cloud SQL and load it into BigQuery. Finally, Looker Studio visualizes the data.
## About Dataset
The dataset contains real-world complaints about financial products and services, with attributes such as product type, issue description, company response, and metadata. This diverse complaints data is the input source for the ETL pipeline and data visualization.
## Architecture
![image](https://github.com/getnkit/Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis/blob/1aae4c7285eaed59480fda3a933bd6ad14cd1346/images/Data%20Architecture.png)
## Implementation
**Step1:** Data profiling with Python\
**Step2:** Store profiled data into Cloud Storage\
**Step3:** Create a database on Cloud SQL and move data from Google Storage to dataset tables\
**Step4:** Create Cloud Composer environment\
**Step5:** Create a table within a dataset on BigQuery\
**Step6:** Run Python script to automated ETL pipeline\
**Step7:** Query data on BigQuery\
**Step8:** Create dashboard to gain insight


