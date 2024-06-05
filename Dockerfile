# When using WSL 2, Docker runs on the Linux kernel inside WSL instead of running on the Windows kernel,
# allowing it to run Linux containers directly without the need to specify the --platform=linux/amd64 flag.
# Based on the Docker Image for Apache Airflow
FROM apache/airflow:2.9.1

# Copy the requirements.txt file to /tmp/requirements.txt in the container
COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

# This package will be installed in the Docker image, separate from virtual environment (venv)
RUN pip install --no-cache-dir airflow-provider-great-expectations==0.2.7