#!/bin/env python3
# definition of strings to use

class Strings:
    def __init__(self,):
        self.user_welcome = "Welcome to the free flight weather forecast application!\nThis application provides MBLUE and ICON weather forecast information.\nYou will need to provide the desired Latitude and Longitude.\nPress enter to exit at any time."
        self.lat_prompt = "Please define the Latitude for the forecast, or press Enter to quit:"
        self.long_prompt = "Please define the Longitude for the forecast, or press Enter to quit:"
        self.model_prompt= "Please select from the following options, or press Enter to quit: \n\tA) ICON Weather Forecast\n\tB) MBLUE Weather Forecast\n\tC) NAM Weather Forecast"
        self.next_prompt = "Select which option you would like to do next: \n\tA) Change Location (Lat/Long entry required)\n\tB) Change Model (no entry required)\n\tC) Change Model and Location (start over)\n\tQ) Quit"
