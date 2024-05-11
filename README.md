# Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis
## Project Overview
This project automates an ETL pipeline using Python. Data is first profiled (reviewed and cleansed) before being loaded into Cloud SQL. Cloud Composer, managing Apache Airflow on GCP, orchestrates the pipeline to transform the data from Cloud SQL and load it into BigQuery. Finally, Looker Studio visualizes the data.
## About Dataset
These are real world complaints received about financial products and services. Each complaint has been labeled with a specific product; therefore, this is a supervised text classification problem. With the aim to classify future complaints based on its content, we used different machine learning algorithms can make more accurate predictions (i.e., classify the complaint in one of the product categories)
## Architecture
![image](https://github.com/getnkit/Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis/blob/1aae4c7285eaed59480fda3a933bd6ad14cd1346/images/Data%20Architecture.png)
## Implementation

