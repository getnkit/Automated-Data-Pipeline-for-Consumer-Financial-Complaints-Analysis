# When using WSL 2, Docker runs on the Linux kernel inside WSL instead of running on the Windows kernel,
# allowing it to run Linux containers directly without the need to specify the --platform=linux/amd64 flag.
FROM apache/airflow:2.9.1

# Copy the requirements.txt file to /tmp/requirements.txt in the container
COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
RUN pip install airflow-provider-great-expectations==0.2.7