import requests
import os
import socket

def get_tweets():
    HOST = socket.gethostbyname(socket.gethostname())

    PORT = 9999

    url = f"http://{HOST}:{PORT}"

    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
