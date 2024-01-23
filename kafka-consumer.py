from kafka import KafkaConsumer
from json import loads
from pyspark.sql import SparkSession
from datetime import datetime
import re
from pyspark.sql.types import *
from pyspark.sql.functions import *
import pandas as pd
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    TimestampType,
)

spark = SparkSession.builder.appName("App").getOrCreate()



kafka_server = ["localhost:9092"]

topic = "tweets"


def check(x):
    try:
        return loads(x.decode("utf-8"))
    except:
        return {"creator": -1}


consumer = KafkaConsumer(
    topic,
    bootstrap_servers=kafka_server,
    auto_offset_reset="earliest",
    group_id=None,
    value_deserializer=check,
)

batch = []
schema = StructType(
    [
        StructField("date", TimestampType(), True),
        StructField("topic", StringType(), True),
        StructField("text", StringType(), True),
        StructField("likes", IntegerType(), True),
        StructField("shares", IntegerType(), True),
        StructField("creator name", StringType(), True),
        StructField("creator email", StringType(), True),
        StructField("creator followers", StringType(), True),
        StructField("creator following", StringType(), True),
        StructField("mentioned name", StringType(), True),
        StructField("mentioned email", StringType(), True),
        StructField("mentioned followers", StringType(), True),
        StructField("mentioned following", StringType(), True),
    ]
)


tweets_location = r"\\wsl.localhost\Ubuntu\home\galal\airflow\dags\data.csv"

email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def clean(row):
    
    date = row["date"]
    topic = row["topic"]
    text = row["text"]
    likes = row["likes"]
    shares = row["shares"]
    creator_name = row["creator name"]
    creator_email = row["creator email"]
    creator_followers = row["creator followers"]
    creator_following = row["creator following"]
    mentioned_name = row["mentioned name"]
    mentioned_email = row["mentioned email"]
    mentioned_followers = row["mentioned followers"]
    mentioned_following = row["mentioned following"]

    if date != None:
        row["date"] = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


    if topic != None:
        if not (topic in ("education", "sports", "food", "games","home", "cooking")):
            row["topic"] = None
    
    
    if text != None:
        row["text"] = re.sub(r"[^\w\s]", "", text).lower().strip()
    
    if likes != None:
        if likes < 0:
            row["likes"] = None
    
    
    if shares != None:
        if shares < 0:
            row["shares"] = None

    if creator_name != None:
        row["creator name"] = re.sub(r"[^\w\s]", "", creator_name).lower().strip()
    

    if creator_email != None:
        if re.fullmatch(email_regex, creator_email):
            row["creator email"] = creator_email
        else:
            row["creator email"] = None


    if creator_followers != None:
        if creator_followers < 0:
            row["creator followers"] = None


    if creator_following != None:
        if creator_following < 0:
            row["creator following"] = None


    if mentioned_name != None:
        row["mentioned name"] = re.sub(r"[^\w\s]", "", mentioned_name).lower().strip()


    if mentioned_email != None:
        if re.fullmatch(email_regex, mentioned_email):
            row["mentioned email"] = mentioned_email
        else:
            row["mentioned email"] = None


    if mentioned_followers != None:
        if mentioned_followers < 0:
            row["mentioned followers"] = None


    if mentioned_following != None:
        if mentioned_following < 0:
            row["mentioned following"] = None

    return row


try:
    print("Waiting for tweets")
    for message in consumer:
        tweet = message.value
        batch.append(tweet)

        if len(batch) == 100:
            tweets_rdd = spark.sparkContext.parallelize(batch)
            tweets_rdd = tweets_rdd.map(clean)
            print(tweets_rdd.collect())
            tweets_df = spark.createDataFrame(tweets_rdd, schema=schema)
            tweets_df = tweets_df.na.fill("null")
            print("Inserting: ", tweets_df.count())
            try:
                old_tweets_df = pd.read_csv(
                    tweets_location,
                )

                print("Before: ", old_tweets_df.shape[0])
                write_df = old_tweets_df.append(tweets_df.toPandas())
            except:
                write_df = tweets_df.toPandas()
                print("Before: ", write_df.shape[0])

            print("Size After: ", write_df.shape[0])
            print("Writing...")
            write_df.to_csv(tweets_location, index=False)
            print("Finished")
            batch = []

except BaseException as e:
    print(e)
exit()
