# Date: 07/20/2024
# Adapted From
# used the code generator and their API documentation to create this code
# Source URL: https://www.meteoblue.com/en/weather-api/index/overview
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import asyncio
import aiohttp
import os
from dotenv import load_dotenv, find_dotenv
import requests

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())
mblue_token = os.environ.get("meteo_blue_token")

def query_mblue(query_lat: float, query_long: float, query_alt: int = 2132, DEBUG: bool = False):

    if DEBUG:
        print(f"query_mblue started for lat: {str(query_lat)}, long: {str(query_long)}")

    url = f"https://my.meteoblue.com/packages/basic-1h_basic-day_wind-15min_wind-1h_wind-3h_air-1h_air-3h?apikey={mblue_token}&lat={query_lat}&lon={query_long}&asl={query_alt}&format=json"
    if DEBUG:
        print(url)

    res = requests.get(url)

    if DEBUG:
        print("Status code = " + str(res.status_code))
        print(res.json())
    if res.status_code != 200:
        print("MBLUE query did NOT run successfully")
        return (False, None)
    print("MBLUE query completed successfully")
    return (True, res.json(),)


if __name__ == "__main__":
    query_mblue(query_lat=35.562, query_long=-106.226, query_alt=2132, DEBUG=True )