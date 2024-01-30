from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import datetime
from airflow.models.dag import DAG
import mysql.connector as mc
import faker
import mysql.connector as mc
import random
import string
import datetime
from wonderwords import RandomSentence
import numpy as np
from kafka import KafkaProducer
from json import dumps, loads
from time import sleep
import requests
import os
import socket
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def _run_producer():
    def get_tweets():
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 9999
        url = "http://192.168.1.17:9999"
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text


    kafka_server = ["localhost:9092"]

    topic = "tweets"

    producer = KafkaProducer(
        bootstrap_servers=kafka_server,
        value_serializer=lambda v: dumps(v).encode("utf-8"),
    )
    print("Connected to Kafka:",producer.bootstrap_connected())


    tweet_list = loads(get_tweets())
    for i in tweet_list:
        print("Producing tweet:", i, type(i))
        producer.send(topic, i)
        producer.flush()
        
    producer.close()
    print("waiting for consumer")
    sleep(20)
    print("Done")

def _create_visuals():
    df = pd.read_csv("/home/galal/airflow/dags/data.csv")
    df['date'] = pd.to_datetime(df['date'])
    numeric_columns = ['likes', 'shares', 'creator followers', 'creator following','mentioned followers', 'mentioned following']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')


    def save_and_close(fig, title):
        fig.savefig(f"/home/galal/airflow/dags/output/{title}.jpg", bbox_inches='tight')
        plt.close()


    grouped_data = df.groupby('date')['likes'].sum().reset_index()

    # Likes Over Time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(grouped_data['date'].values, grouped_data['likes'].values, label="Likes")
    ax.set_title('Likes Over Time (Grouped by Date)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Likes')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    save_and_close(fig, "LikesOverTime")

    grouped_data = df.groupby('date')['shares'].sum().reset_index()

    # Shares Over Time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(grouped_data['date'].values, grouped_data['shares'].values, label='Shares')
    ax.set_title('Shares Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Shares')
    ax.legend()
    save_and_close(fig, "SharesOverTime")

    # Distribution of creator followers
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(df['creator followers'], vert=False)
    ax.set_title('Distribution of creator followers')
    save_and_close(fig, "DistOfCreatorFollowers")

    # Relation between likes and mentioned followers
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df['likes'].values, df['mentioned followers'].values, alpha=0.7)
    ax.set_title('Relation between likes and mentioned followers')
    ax.set_xlabel('Likes')
    ax.set_ylabel('Mentioned Followers')
    save_and_close(fig, "RelationLikesMentionedFollowers")

    # Likes Histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["likes"].values)
    ax.set_title("Likes Histogram")
    ax.set_xlabel('Likes')
    ax.set_ylabel('Frequency')
    save_and_close(fig, "Likes")

    # Shares Histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["shares"].values)
    ax.set_title("Shares Histogram")
    ax.set_xlabel('Shares')
    ax.set_ylabel('Frequency')
    save_and_close(fig, "Shares")

    # User Post Histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df['creator name'].value_counts().values)
    ax.set_title("User Post Histogram")
    ax.set_xlabel('Number of Posts')
    ax.set_ylabel('Frequency')
    save_and_close(fig, "CreatorName")

with DAG(
    dag_id="galalDag",
    schedule='@hourly',
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
) as dag:

    produce_tweets_task = PythonOperator(
        task_id="produce_tweets",
        python_callable=_run_producer,
        dag=dag
    )

    create_visuals_task = PythonOperator(
        task_id="create_visuals",
        python_callable=_create_visuals,
        dag=dag
    )

    produce_tweets_task >> create_visuals_task