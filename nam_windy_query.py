# Date: 08/04/2024
# used the code generator and their API documentation to create this code
# Source URL: https://api.windy.com/point-forecast/docs
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
import requests
import zmq


# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())
nam_token = os.environ.get("nam_token")

def query_nam(query_lat, query_long, query_alt: int = 2132, DEBUG: bool = False):
    query_lat = str(query_lat).strip()
    query_long = str(query_long).strip()
    body = {
    "lat": query_lat,
    "lon": query_long,
    "model": "namConus",
    "parameters": ["wind", "windGust", "precip", "cape", "temp", "dewpoint", "rh", "pressure"],
    "levels": [ "surface", ],
    "key": nam_token
    }
    if DEBUG:
        print(f"query_nam started for lat: {query_lat}, long: {query_long}")
    url = f"https://api.windy.com/api/point-forecast/v2"
    if DEBUG:
        print(url)

    res = requests.post(url, json=body)

    if DEBUG:
        print("Status code = " + str(res.status_code))
        print(res.json())
    if res.status_code != 200:
        print("NAM query did NOT run successfully")
        return False, None
    print("NAM query completed successfully")
    return True, res.json()


def setup_server(ip: str = 'localhost', port: int = 5559, DEBUG: bool = False):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{ip}:{port}")
    print(f"**NAM SERVICE: Connecting to tcp://{ip}:{port}")
    
    while True:
        #  Wait for request from client
        message = socket.recv().decode('utf-8')
        if DEBUG:
            print(f"**NAM SERVICE: Received request: {message}")
        lat = message.split(",")[0]
        long = message.split(",")[1]
        response, send_message = query_nam(lat, long, DEBUG=True)
        if not response:
            print("**NAM SERVICE: Error communicating to the MBLUE API")
            return
        send_message = bytes(f"{send_message}", 'utf-8')

        new_message = "**NAM SERVICE: Replying - " + str(send_message[:10])
        print(f"{new_message}")

        #  Send reply back to client
        socket.send(send_message)
        if DEBUG:
            print("**NAM SERVICE: sent new message!")

if __name__ == "__main__":
    setup_server(DEBUG=True)
    #query_nam(query_lat=35.562, query_long=-106.226, query_alt=2132, DEBUG=True )