# Data Pipeline on GCP for Consumer Financial Complaints Analysis
## Project Overview
This project focuses on building and automating a data pipeline with Apache Airflow. Before ingesting data into the automated data pipeline, it undergoes data profiling (review and cleansing) and is then uploaded to Cloud SQL (MySQL) using a Python. Subsequently, the automated data pipeline extracts data from MySQL, transforms the data, and loads it into Google Cloud Storage (GCS) to ingest the data into BigQuery. Finally, a Consumer Financial Complaints Dashboard is developed using Looker Studio.
## About Dataset
This dataset consists of real-world complaints about financial products and services, including details such as product type, issue description, company response, and other metadata. These complaints are published after the company responds, or after 15 days from the date of receipt, whichever comes first. By voicing their opinions and complaints, consumers help improve the quality and efficiency of the financial marketplace.
## Architecture
![image](https://github.com/getnkit/Data-Pipeline-on-GCP-for-Consumer-Financial-Complaints-Analysis/blob/dc1de1502b228873f33218c5365b7ad8f5176fe4/images/Data%20Architecture.png)
## Implementation
### Step 1: Data profiling using Python on Google Colab
### Step 2: Set up a Virtual Environment in Python
**Using virtual environments (venv) in Python helps isolate project dependencies and prevent conflicts between projects or system packages.**

Creates a Python Virtual Environment named "ENV", isolating project dependencies from the global Python environment.
```
python -m venv ENV
```
Activates the Python Virtual Environment named "ENV", allowing you to work within that isolated environment.
```
ENV\Scripts\activate
```
Installs the specified Python packages into the current Python environment and then saves a list of all installed packages to a requirements.txt file.
```
pip install pandas>=2.2.2 pymysql>=1.0.2
pip freeze > requirements.txt
```
Alternatively, packages to be installed can be directly defined in the requirements.txt file. Then, install all the Python packages listed in the requirements.txt file.
```
pip install -r requirements.txt
```
### Step 3: Create a MySQL Database with Cloud SQL
### Step 4: Import profiled data into MySQL Database using Python
### Step 5: Create a bucket on Google Cloud Storage (GCS) and a dataset on BigQuery for Data pipeline
### Step 6: Install and Configure Airflow Using Docker Container
Fetching docker-compose.yaml to deploy Airflow on Docker Compose
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.1/docker-compose.yaml'
```
Setting the right Airflow user
```
mkdir -p ./dags ./logs ./plugins ./config
echo "AIRFLOW_UID=50000" > .env
```
Create a Dockerfile to describe how to create, then build a Docker image
```
docker build -t custom-airflow-image:2.9.1 .
```
Configure docker-compose yaml, then run the docker-compose command to run Docker containers based on the settings described in a docker-compose.yaml file

```
docker compose up airflow-init
docker compose up
```
Access to Airflow UI
```
http://localhost:8080/
```
### Step 7: Set up Connection & Variables in Airflow
### Step 8: Create Python DAG in Airflow
**Step 8.1: Importing Modules**
- Import necessary modules and libraries for the DAG.

**Step 8.2: Extract Data from MySQL**
- Connects to a MySQL database using MySqlHook.
- Fetches data from two tables and loads them into Pandas DataFrames.
- Saves these DataFrames as CSV files in the specified directory.

**Step 8.3: Transform Data**
- Reads the previously saved CSV files into Pandas DataFrames.
- Converts necessary columns to string type to ensure proper merging.
- Merges the two DataFrames.
- Drops redundant columns and rearranges the columns.
- Saves the transformed DataFrame as a CSV file in the specified directory.

**Step 8.4: Load Data to Google Cloud Storage (GCS)**
- Prepares Google Cloud Storage credentials from Airflow Variables.
- Initializes a Google Cloud Storage client using the credentials.
- Specifies the bucket name and file path for uploading the transformed CSV file.
- Uploads the file to the specified GCS bucket and path.

**Step 8.5: Load Data from GCS to BigQuery**
- Prepares Google BigQuery credentials from Airflow Variables.
- Initializes a BigQuery client using the credentials.
- Specifies the BigQuery table ID and job configuration for loading the CSV file from GCS.
- Loads the CSV file from GCS to the specified BigQuery table, using the configured job settings (e.g., skipping the first row, auto-detecting schema, etc.).

**Step 8.6: Airflow DAG Definition**
- Defines the DAG name.
- Sets the start date to one day ago and schedules the DAG to run once (@once).
- Tags the DAG with "financial", "mysql", and "bigquery".
- Create task specifies an individual step in a workflow.
- Set up dependencies or the order in which tasks should be executed.

### Step 9: Copy the DAG file from local machine to Airflow container
```
docker cp <source_path> <container_id>:/opt/airflow/dags/
```
### Step 10: Run the DAG file in the Airflow UI
Unpause the DAG
```
docker exec -it <airflow-webserver-container_id> airflow dags unpause <dag_id>
```
Trigger the DAG
```
docker exec -it <airflow-webserver-container_id> airflow dags trigger <dag_id>
```
Monitor the DAG

![image](https://github.com/getnkit/Data-Pipeline-on-GCP-for-Consumer-Financial-Complaints-Analysis/blob/cb910a1e2309041b475ead4b1249a2b316f8f907/images/Data%20Pipeline%20with%20Airflow.png)

After the workflow process is completed, the data will be loaded into BigQuery.

![image](https://github.com/getnkit/Data-Pipeline-on-GCP-for-Consumer-Financial-Complaints-Analysis/blob/6f431fbf35a3fe1eb3c7136b952e14f11a8c3baf/images/Loaded%20data%20into%20BigQuery.png)
### Step 11: Create Consumer Financial Complaints Dashboard using Looker Studio
![image](https://github.com/getnkit/Automated-ETL-Pipeline-for-Consumer-Financial-Complaints-Analysis/blob/761e209eb5ff580afadef3da504393fcd835949a/images/Consumer%20Financial%20Complaints%20Dashboard.jpg)
#### Insight Gained
- 100,000 is the total number of complaints received.
- 97.4% of responses by the bank were delivered on time.
- Around 19,800 complaints were related to Customer Dispute Cases, which is approximately 20% of the total.
- The top issue for consumers was "Incorrect information on credit report", followed closely by "Loan modification", "collection", "foreclosure" at a similar rate.
- The products/services with the highest number of complaints were "Mortgage", "Debt collection", and "Credit reporting".
- Around 70% of the complaints were submitted via "the website".
- The majority of company responses to consumers had a status of "Closed with explanation".
- For complaints arising from different states, a "Bubble map" was created, where larger bubbles represent states with a higher number of complaints, and smaller bubbles represent states with fewer complaints. The bubble sizes range from larger to smaller, corresponding to the number of complaints.
### [Optional] Step 12: Create CI pipeline using GitHub Actions
Create a workflow file named ```docker-image.yml``` within the ```.github/workflows/``` directory. This CI pipeline will be triggered whenever a new push is made to the main branch of the repository.

![image](https://github.com/getnkit/Data-Pipeline-on-GCP-for-Consumer-Financial-Complaints-Analysis/blob/dbe40347512a2795980c0c70ea6bcc1d1f3bbac7/images/CI%20Pipeline.jpg)
After the job completes, the built Docker image will be pushed to the specified Docker Hub repository.
Docker images stored in a container registry can be utilized in various ways, including:
- Deploying containers from the image on local machines or servers
- Deploying instances or using the image as a base image for instance templates on cloud platforms
- Deploying containers in a Kubernetes cluster for scalable and orchestrated application deployment

![image](https://github.com/getnkit/Data-Pipeline-on-GCP-for-Consumer-Financial-Complaints-Analysis/blob/862a7781a36225ff3752996057414c1224f2a729/images/Docker%20Hub%20repository.jpg)

In the early stages of development, building Docker images manually (Step 6) or using Docker Compose directly can be more suitable for flexibility in experimentation and debugging. GitHub Actions can be utilized when the codebase becomes more stable and requires increased automation, which helps save time and reduce errors from repetitive tasks.

