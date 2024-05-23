import configparser
import pandas as pd

# Specifies the configuration file path
CONFIG_FILE = "db.conf"

# Parses the configuration file
parser = configparser.ConfigParser()
parser.read(CONFIG_FILE)

# Retrieves database connection details
database = parser.get("mysql_config", "database")
user = parser.get("mysql_config", "username")
password = parser.get("mysql_config", "password")
host = parser.get("mysql_config", "host")
port = parser.get("mysql_config", "port")

# Constructs the database URI
uri = f"mysql+pymysql://{user}:{password}@{host}/{database}"

# Reads data from CSV files
df = pd.read_csv("consumer_data_profiled.csv")
df = pd.read_csv("state_name_profiled.csv")

# Imports data into the MySQL database
df.to_sql("consumer_data_profiled", con=uri, if_exists="replace", index=False)
df.to_sql("state_name_profiled", con=uri, if_exists="replace", index=False)

print(f"Imported data successfully")