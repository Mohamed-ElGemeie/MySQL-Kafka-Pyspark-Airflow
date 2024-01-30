from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket
import json
import random
import mysql.connector as mc
from socketserver import ThreadingMixIn
import threading

HOST = socket.gethostbyname(socket.gethostname())
print(HOST)
PORT = 9999
max_users = 1000
max_tweets = 10000
amount_of_tweets = 100


class server(BaseHTTPRequestHandler):
    def do_POST(self):
        response_body = []

        try:
            tweet_ids = random.sample(range(1, max_tweets + 1), amount_of_tweets)
            with mc.connect(
                host="localhost",
                user="root",
                passwd="KOKOWaWa1Ak9",
                database="twitter",
            ) as db:
                cursor = db.cursor()
                for i in tweet_ids:
                    temp_tweet = {
                        "date": None,
                        "topic": None,
                        "text": None,
                        "likes": None,
                        "shares": None,
                        "creator name": None,
                        "creator email": None,
                        "creator followers": None,
                        "creator following": None,
                        "mentioned name": None,
                        "mentioned email": None,
                        "mentioned followers": None,
                        "mentioned following": None,
                    }
                    # sql = f"""SELECT * FROM `twitter`.`tweets` WHERE `id`= {i}"""
                    sql = f"""SELECT t.date as "date", t.topic as "topic", t.text as "text", t.likes as "likes", t.shares as "shares",
 u.name as "creator", u.email as "creator name", u.followers as "creator followers", u.following as "creator following",
 m.name as "mentioned name",m.email as "mentioned email", m.followers as "mentioned followers", m.following as "mentioned following"
FROM `twitter`.`tweets` t
join `twitter`.`users` u
on  u.id = t.creator
left join `twitter`.`users` m
on m.id = t.mentions
WHERE t.id = {i}"""
                    cursor.execute(sql)
                    tweet = cursor.fetchone()
                    temp_tweet["date"] = tweet[0]
                    temp_tweet["topic"] = tweet[1]
                    temp_tweet["text"] = tweet[2]
                    temp_tweet["likes"] = tweet[3]
                    temp_tweet["shares"] = tweet[4]
                    temp_tweet["creator name"] = tweet[5]
                    temp_tweet["creator email"] = tweet[6]
                    temp_tweet["creator followers"] = tweet[7]
                    temp_tweet["creator following"] = tweet[8]
                    temp_tweet["mentioned name"] = tweet[9]
                    temp_tweet["mentioned email"] = tweet[10]
                    temp_tweet["mentioned followers"] = tweet[11]
                    temp_tweet["mentioned following"] = tweet[12]

                    response_body.append(temp_tweet)
        except:
            self.send_error(400, "Failed")
            return

        json_data = json.dumps(response_body, indent=4, default=str)
        print("Sending Tweets:", json_data)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json_data.encode())



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
 """Handle requests in a separate thread."""

if __name__ == "__main__":
 
    webServer = ThreadedHTTPServer((HOST, PORT), server)
    print(f"Server started http://{HOST}:{PORT}")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
