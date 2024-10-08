# Date: 07/20/2024
# Adapted From
# used the code generator and their API documentation to create this code
# Source URL: https://open-meteo.com/en/docs/ecmwf-api
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import pprint
import zmq


def query_icon(query_lat: float, query_long: float, DEBUG: bool = False):

    if DEBUG:
        print(f"query_icon started for lat: {str(query_lat)}, long: {str(query_long)}")

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": query_lat,
        "longitude": query_long,
        "models": "icon_seamless",
        "timezone": "MST",
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "pressure_msl",
            "surface_pressure",
            "wind_speed_10m",
            "wind_speed_100m",
            "wind_direction_10m",
            "wind_direction_100m",
            "surface_temperature",
            "cape",
        ],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "forecast_days": 7,
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. To-do: add a for-loop for multiple locations or weather models
    response = responses[0]
    if DEBUG:
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(4).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(5).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(6).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(7).ValuesAsNumpy()
    hourly_wind_speed_100m = hourly.Variables(8).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(9).ValuesAsNumpy()
    hourly_wind_direction_100m = hourly.Variables(10).ValuesAsNumpy()
    hourly_surface_temperature = hourly.Variables(11).ValuesAsNumpy()
    hourly_cape = hourly.Variables(12).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=False),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=False),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["pressure_msl"] = hourly_pressure_msl
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_direction_100m"] = hourly_wind_direction_100m
    hourly_data["surface_temperature"] = hourly_surface_temperature
    hourly_data["cape"] = hourly_cape

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    #print(hourly_dataframe)

    if DEBUG:
        pprint.pp(hourly_dataframe.to_dict())

    print("OpenMeteo ICON query completed successfully")
    return True, str(hourly_dataframe.to_dict())

def setup_server(ip: str = 'localhost', port: int = 5556, DEBUG: bool = False):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{ip}:{port}")
    print(f"**ICON SERVICE: Connecting to tcp://{ip}:{port}")
    
    while True:
        #  Wait for request from client
        message = socket.recv().decode('utf-8')
        if DEBUG:
            print(f"**ICON SERVICE: Received request: {message}")
        lat = message.split(",")[0]
        long = message.split(",")[1]
        response, send_message = query_icon(lat, long, DEBUG=True)
        if not response:
            print("Error communicating to the OPENMETEO ICON API")
            return
        send_message = bytes(send_message, 'utf-8')

        new_message = "**ICON SERVICE: Replying - " + str(send_message[:10])
        if DEBUG:
            print(f"{new_message}")

        #  Send reply back to client
        socket.send(send_message)
        if DEBUG:
            print("**ICON SERVICE: sent new message!")

if __name__ == "__main__":
    setup_server(DEBUG=True)
    #query_icon(query_lat=35.562, query_long=-106.226, DEBUG=True )