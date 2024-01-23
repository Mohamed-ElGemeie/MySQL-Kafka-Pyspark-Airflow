import faker
import mysql.connector as mc
import random
import string
import datetime
from wonderwords import RandomSentence
import numpy as np


s = RandomSentence()
fake = faker.Faker()
max_users = 1000
max_tweets = 10000

lower_limit = datetime.datetime(2024, 1, 1)
upper_limit = datetime.datetime(2002, 1, 1)
likess = list(range(1, 420))
likess_prob = list(np.linspace(0.9, 0.1, len(likess)))
sharess = list(range(1, 580))
sharess_prob = list(np.linspace(0.9, 0.1, len(sharess)))
topics = ["food", "sports", "education", "games", "home", "cooking"]


def generate_tweet():
    total_seconds = (upper_limit - lower_limit).total_seconds()

    random_seconds = random.uniform(0, total_seconds)

    random_datetime = lower_limit + datetime.timedelta(seconds=random_seconds)

    topic = random.choices(topics, weights=[0.5, 0.1, 0.3, 0.1, 0.1, 0.1])[0]

    likes = random.choices(likess, weights=likess_prob)[0]

    shares = random.choices(sharess, weights=sharess_prob)[0]

    text = fake.text()

    mentions = random.sample(range(1, max_users + 1), random.randint(0, 1))
    if len(mentions) != 0:
        mentions = mentions[0]
    else:
        mentions = None

    return (random_datetime, topic, text, mentions, likes, shares)


# Function to generate a random user
def generate_user():
    name = fake.name()
    email = fake.email()
    followers = random.randint(0, max_users)
    following = random.randint(0, max_users)
    return name, email, followers, following


with mc.connect(
    host="localhost", user="root", passwd="KOKOWaWa1Ak9", database="twitter"
) as db:
    cursor = db.cursor()

    cursor.execute("""ALTER TABLE `twitter`.`users` AUTO_INCREMENT = 1""")
    cursor.execute("""ALTER TABLE `twitter`.`tweets` AUTO_INCREMENT = 1""")
    db.commit()
    for i in range(max_users):
        name, email, followers, following = generate_user()
        sql = """INSERT INTO `twitter`.`users` (`name`,`email`, `followers`, `following`) VALUES (%s,%s,%s,%s);"""
        val = (name, email, followers, following)
        cursor.execute(sql, val)
    db.commit()
    for i in range(max_tweets):
        creator = random.randint(1, max_users)
        date, topic, text, mentions, likes, shares = generate_tweet()
        sql = "INSERT INTO tweets (date, topic, text, mentions, creator, likes, shares) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (date, topic, text, mentions, creator, likes, shares)
        cursor.execute(sql, val)
    db.commit()

print("DB was seeded successfully")