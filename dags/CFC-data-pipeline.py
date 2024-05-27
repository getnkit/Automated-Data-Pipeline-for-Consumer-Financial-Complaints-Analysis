# Consumer Financial Complaints data pipeline

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.utils.dates import days_ago
import pandas as pd
from google.cloud import bigquery, storage
from google.oauth2 import service_account


def extract_from_mysql():
    # Connect to the MySQL database using MySqlHook
    mysqlserver = MySqlHook(mysql_conn_id="cloud_sql_mysql")
    conn = mysqlserver.get_conn()

    # Fetch data from the tables and convert them into Pandas DataFrames
    df1 = pd.read_sql("SELECT * FROM consumer_data_profiled LIMIT 100000", con=conn)
    df2 = pd.read_sql("SELECT * FROM state_name_profiled", con=conn)

    # Warning! Avoid using XComs Backend for passing big data,
    # because Airflow, as an orchestrator, cannot efficiently handle big data processing like Spark.
    # The maximum data size of XComs in Airflow depends on the database used (for MySQL, it is 64 KB).

    # Uses MySqlHook to retrieve data from MySQL, then stores the data in a CSV file instead of passing it through XComs.
    df1.to_csv("/opt/airflow/dags/consumer_data_profiled.csv", index=False)
    df2.to_csv("/opt/airflow/dags/state_name_profiled.csv", index=False)

def transform_data():
    df1 = pd.read_csv("/opt/airflow/dags/consumer_data_profiled.csv")
    df2 = pd.read_csv("/opt/airflow/dags/state_name_profiled.csv")

    # Convert the columns to string type to ensure correct merging
    df1['State code'] = df1['State code'].astype(str)
    df2['State abbreviation'] = df2['State abbreviation'].astype(str)

    df3 = df1.merge(df2, how="left", left_on="State code", right_on="State abbreviation")
    df3 = df3.drop(columns=['State abbreviation'])

    # Rearrange columns to place 'State name' next to 'State code'
    cols = df3.columns.tolist()
    state_code_index = cols.index('State code')
    new_cols = cols[:state_code_index + 1] + ['State name'] + cols[state_code_index + 1:]
    df3 = df3[new_cols]
    print(df3.head())

    df3.to_csv("/opt/airflow/dags/consumer_data_transformed.csv", index=False)

def load_to_gcs():
    BUSINESS_DOMAIN = "financial"
    location = "us-central1"

    # Prepare and Load Credentials to Connect to GCP Services
    # IAM roles = roles/storage.objectCreator 

    # Solution 1: Store credentials in Local Filesystem, Easy and convenient for creation and usage
    # keyfile_gcs = "/opt/airflow/dags/consumer-financial-complaints-e11184689944.json"
    # service_account_info_gcs = json.load(open(keyfile_gcs))

    # Solution 2: Store credentials in Airflow Variable, Secure and centrally managed
    service_account_info_gcs = Variable.get(
        "keyfile_gcs_secret",
        deserialize_json=True,
    )
    credentials_gcs = service_account.Credentials.from_service_account_info(
        service_account_info_gcs
    )

    project_id = Variable.get("consumer_financial_complaints")

    # Load data from Local to GCS
    bucket_name = Variable.get("financial_bucket")
    storage_client = storage.Client(
        project=project_id,
        credentials=credentials_gcs,
    )
    bucket = storage_client.bucket(bucket_name)

    file_path = "/opt/airflow/dags/consumer_data_transformed.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/consumer_data_transformed.csv"

    # Create a blob object that references the file to be uploaded to the bucket
    blob = bucket.blob(destination_blob_name)
    # Upload the file from the file_path to GCS under the destination_blob_name
    blob.upload_from_filename(file_path, timeout=3600)

def load_from_gcs_to_bigquery():
    BUSINESS_DOMAIN = "financial"
    location = "us-central1"

    bucket_name = Variable.get("financial_bucket")
    destination_blob_name = f"{BUSINESS_DOMAIN}/consumer_data_transformed.csv"

    # Prepare and Load Credentials to Connect to GCP Services
    # IAM roles = roles/bigquery.dataEditor, roles/bigquery.jobUser, roles/storage.objectViewer

    # keyfile_bigquery = "/opt/airflow/dags/consumer-financial-complaints-ce66ead1df4e.json"
    # service_account_info_bigquery = json.load(open(keyfile_bigquery))

    service_account_info_bigquery = Variable.get(
        "keyfile_bigquery_secret",
        deserialize_json=True,
    )
    credentials_bigquery = service_account.Credentials.from_service_account_info(
        service_account_info_bigquery
    )

    project_id = Variable.get("consumer_financial_complaints")

    # Load data from GCS to BigQuery
    bigquery_client = bigquery.Client(
        project=project_id,
        credentials=credentials_bigquery,
        location=location,
    )

    table_id = f"{project_id}.financial_dataset.consumer_data"

    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )

    job = bigquery_client.load_table_from_uri(
        f"gs://{bucket_name}/{destination_blob_name}",
        table_id,
        job_config=job_config,
        location=location,
    )

    job.result()


with DAG(
    "cfc-data-pipeline-v3",
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=["financial", "mysql", "bigquery"],
) as dag:

    t1 = PythonOperator(
        task_id="extract_from_mysql",
        python_callable=extract_from_mysql,
    )

    t2 = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    t3 = PythonOperator(
        task_id="load_to_gcs",
        python_callable=load_to_gcs,
    )

    t4 = PythonOperator(
        task_id="load_from_gcs_to_bigquery",
        python_callable=load_from_gcs_to_bigquery,
    )

    t1 >> t2 >> t3 >> t4