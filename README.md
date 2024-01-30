<br />
<h1 align="center">Visualizing Tabular Data Samples Using Big Data Tools</h1>
<p align="center">
    This project involves a Kafka and PySpark pipeline that utilizes a MySQL database and Airflow for scheduling.
    <br />
    <br />
    <br />
</p>
</div>

<details>
  <summary><strong>Table of Contents</strong></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This project simulates the distribution of tabular data samples across different mediums to be processed for visualization. The data was randomly self-generated in a MySQL database and passed through a Kafka topic, then through PySpark, and finally through some Pandas visualizations. All of these processes were scheduled hourly by Airflow.

### Built With

* [MySQL](https://www.mysql.com/)
* [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)
* [Pandas](https://pandas.pydata.org/)
* [AirFlow](https://airflow.apache.org/)
* [Kafka](https://kafka.apache.org/)
* [ZooKeeper](https://zookeeper.apache.org/)

<!-- GETTING STARTED -->
## Getting Started

To get the project working, you must complete the following steps:

- Start Python Webserver
- Start Kafka Server
- Start ZooKeeper Server
- Start MySQL Server and create the database
- Start Kafka Consumer
- Start AirFlow

### Prerequisites

Ensure you have the following installed:

* [Pyspark](https://www.machinelearningplus.com/pyspark/install-pyspark-on-windows/) on your local Windows machine
* [Python 3.9](https://www.python.org/downloads/release/python-390/)
* [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
* [Docker](https://docs.docker.com/engine/install/)
* [AirFlow](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html) on WSL

### Installation

1. Follow all the instructions mentioned in [commands.txt](https://github.com/Mohamed-ElGemeie/MySQL-Kafka-Pyspark-Airflow-Pipeline/blob/main/commands.txt)
2. Run the webserver
3. Run the consumer
4. Run the Airflow server
5. Manually trigger to check if everything works

<!-- USAGE EXAMPLES -->
## Usage

You may edit the database seeder to transmit your own data and initiate multiple producers or machines on a Kafka cluster to receive these samples.

<!-- CONTACT -->
## Contact

Mohamed Galal Elgemeie - [LinkedIn](https://www.linkedin.com/in/mohamed-elgemeie) - mgalal2002@outlook.com

Project Link: [MySQL-Kafka-Pyspark-Airflow-Pipeline](https://github.com/Mohamed-ElGemeie/MySQL-Kafka-Pyspark-Airflow-Pipeline)

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Eng. Tawfek for his very helpful and considerate mentoring
* Dr. Walaa for giving us this great opportunity

<p align="right">(<a href="#top">back to top</a>)</p>