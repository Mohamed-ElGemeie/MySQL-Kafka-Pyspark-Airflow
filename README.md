# MySQL-Kafka-Pyspark-Airflow

- create and seed twitter alike database using python scripts on local machine
- run a docker Kafka server, MySQL server, Airflow, pyspark context
- create a kafka topic called tweets
- host backend server that retrives data from the MySQL database
- Kafka producer sends data from the backend server to the Kafka topic
- Kafka consumer gets the data from the Kafka topic and does preprocessing in Pyspark
- write this data to a csv file which is stored in wsl
- airflow runs a python file that extracts visualz from this csv file

MySQL -> Backend Server -> Kafka producer -> Kafka consumer -> Pyspark -> .csv -> create Visuals
