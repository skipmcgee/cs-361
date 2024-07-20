#!/bin/env python3
import time
import zmq
from strings import Strings
from openmeteo_icon_query import query_icon
from meteo_blue_query import query_mblue

s = Strings()
breakout = 0

def my_ui(DEBUG: bool = False):

    def greet_user():
        print(s.user_welcome)
        time.sleep(1)

    def lat_long():
        print(s.lat_prompt)
        lat_resp = input()
        if 'Q' in lat_resp:
            breakout = 1
            return
        if len(lat_resp) == 0:
            return False, False
        print(s.long_prompt)
        long_resp = input()
        if 'Q' in long_resp:
            breakout = 1
            return
        if len(long_resp) == 0:
            return False, False
        return lat_resp, long_resp

    def pick_models(get_lat, get_long):
        print(s.model_prompt)
        model_resp = input()
        if 'Q' in model_resp:
            breakout = 1
            return
        if not 'A' in model_resp and not 'B' in model_resp:
            breakout = 1
            return False
        if model_resp == 'A':
            print(query_icon(get_lat, get_long))
        elif model_resp == 'B':
            print(query_mblue(get_lat, get_long))

    def pick_next():
        print(s.next_prompt)
        next_resp = input()
        if 'Q' in next_resp:
            breakout = 1
            return
        if not 'A' in next_resp and not 'B' in next_resp and not 'C' in next_resp:
            return False
        return next_resp

    greet_user()

    lat_resp, long_resp = lat_long()
    if lat_resp == False or long_resp == False:
        breakout = 1
        return
    model_resp = pick_models(lat_resp, long_resp)
    if model_resp == False:
        breakout = 1
        return
    next_resp = pick_next()
    if next_resp == 'A':
        print("Change Location")
    elif next_resp == "B":
        print("Change Model")
    elif next_resp == 'C':
        my_ui()
    else:
        return



if __name__ == '__main__':
    my_ui(DEBUG = True)