# Date: 07/20/2024
# Adapted From
# used the code generator and their API documentation to create this code
# Source URL: https://www.meteoblue.com/en/weather-api/index/overview
import pandas as pd
import asyncio
import aiohttp
import os
from dotenv import load_dotenv, find_dotenv
import requests
import zmq


# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())
mblue_token = os.environ.get("meteo_blue_token")

def query_mblue(query_lat, query_long, query_alt: int = 2132, DEBUG: bool = False):
    query_lat = str(query_lat).strip()
    query_long = str(query_long).strip()
    if DEBUG:
        print(f"query_mblue started for lat: {query_lat}, long: {query_long}")
    url = f"https://my.meteoblue.com/packages/basic-1h_basic-day_wind-15min_wind-1h_wind-3h_air-1h_air-3h?apikey={mblue_token}&lat={query_lat}&lon={query_long}&asl={query_alt}&format=json"
    if DEBUG:
        print(url)

    res = requests.get(url)

    if DEBUG:
        print("Status code = " + str(res.status_code))
        print(res.json())
    if res.status_code != 200:
        print("MBLUE query did NOT run successfully")
        return False, None
    print("MBLUE query completed successfully")
    return True, res.json()


def setup_server(ip: str = 'localhost', port: int = 5555, DEBUG: bool = False):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{ip}:{port}")
    print(f"**MBLUE SERVICE: Connecting to tcp://{ip}:{port}")
    
    while True:
        #  Wait for request from client
        message = socket.recv().decode('utf-8')
        if DEBUG:
            print(f"**MBLUE SERVICE: Received request: {message}")
        lat = message.split(",")[0]
        long = message.split(",")[1]
        response, send_message = query_mblue(lat, long, DEBUG=True)
        if not response:
            print("**MBLUE SERVICE: Error communicating to the MBLUE API")
            return
        send_message = bytes(f"{send_message}", 'utf-8')

        new_message = "**MBLUE SERVICE: Replying - " + str(send_message[:10])
        print(f"{new_message}")

        #  Send reply back to client
        socket.send(send_message)
        if DEBUG:
            print("**MBLUE SERVICE: sent new message!")

if __name__ == "__main__":
    setup_server(DEBUG=True)
    #query_mblue(query_lat=35.562, query_long=-106.226, query_alt=2132, DEBUG=True )