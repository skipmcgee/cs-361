#!/bin/env python3
import time
import zmq
from strings import Strings
import sys

s = Strings()
breakout = 0
context = zmq.Context()


def talk_to_service(send_message: str, ip: str = 'localhost', port: int = 5555, DEBUG: bool = False):
    #  Socket to talk to server
    if DEBUG:
        print(f"**UI: Connecting to tcp://{ip}:{port}")
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{ip}:{port}")

    send_message = bytes(send_message, 'utf-8')

    # Send a message
    if DEBUG:
        print(f"**UI: Sending message '{send_message}'")
    socket.send(send_message)
    if DEBUG:
        print(f"**UI: waiting for response to request")
        
    #  Get the reply.
    message = socket.recv().decode('utf-8')
    if DEBUG:
        print(f"**UI: Received reply: {message}")

    return message


def greet_user():
    print(s.user_welcome)
    time.sleep(2)

def check_lat(lat_to_check: float):
    if 90 >= lat_to_check >= -90:
        return True
    return False

def check_long(long_to_check: float):
    if 180 >= long_to_check >= -180:
        return True
    return False

def lat_long():
    print(s.lat_prompt)
    lat_resp = input()
    if 'Q' in lat_resp:
        sys.exit(0)
    if len(lat_resp) == 0:
        sys.exit(0)
    print(s.long_prompt)
    long_resp = input()
    if 'Q' in long_resp:
        sys.exit(0)
    if len(long_resp) == 0:
        sys.exit(0)
    # check to make sure parameters are correct
    correct_formatting = False
    if check_lat(float(lat_resp)) and check_long(float(long_resp)):
        correct_formatting = True
    return correct_formatting, lat_resp, long_resp


def pick_models():
    print(s.model_prompt)
    model_resp = input()
    if len(model_resp) == 0:
        sys.exit(0)
    if 'Q' in model_resp:
        sys.exit(0)
    if not 'A' in model_resp and not 'B' in model_resp and not 'C' in model_resp:
        sys.exit(0)

    return model_resp


def pick_next():
    print(s.next_prompt)
    next_resp = input()
    if 'Q' in next_resp:
        sys.exit(0)
    if not 'A' in next_resp and not 'B' in next_resp and not 'C' in next_resp:
        sys.exit(0)
    return next_resp


def my_ui(lat_resp = False, long_resp = False, model_resp = False, DEBUG: bool = False):

    # only prompt at first run
    if not lat_resp and not long_resp and not model_resp:
        greet_user()
        # provide and ispirational quote:
        print("Here is an inspirational quote for motivation:")
        quote = talk_to_service(send_message='Please quote me', port=5558)
        print(f'"{quote}"')
    if not lat_resp or not long_resp:
        correct, lat_resp, long_resp = lat_long()
        while not correct:
            print("UI: lat/long entered incorectly, please try again!")
            correct, lat_resp, long_resp = lat_long()
        if not lat_resp or not long_resp:
            print("UI: exiting early, no lat/long")
            sys.exit(0)
    if not model_resp:
        model_resp = pick_models()
        if not model_resp:
            print("UI: exiting early, no model picked")
            sys.exit(0)

    if model_resp == 'A':
        print(talk_to_service(send_message=f"{lat_resp},{long_resp}", port=5556, DEBUG=DEBUG))
    elif model_resp == 'B':
        print(talk_to_service(send_message=f"{lat_resp},{long_resp}", port=5555, DEBUG=DEBUG))
    elif model_resp == 'C':
        print(talk_to_service(send_message=f"{lat_resp},{long_resp}", port=5559, DEBUG=DEBUG))

    next_resp = pick_next()
    print("UI: next response is " + next_resp)
    if next_resp == 'A':
        if DEBUG:
            print("Change Location selected")
        my_ui(lat_resp=False, long_resp=False, model_resp=model_resp, DEBUG=DEBUG)
    elif next_resp == "B":
        if DEBUG:
            print("Change Model selected")
        my_ui(lat_resp=lat_resp, long_resp=long_resp, model_resp=False, DEBUG=DEBUG)


def wrapper():
    while True:
        my_ui(lat_resp=False, long_resp=False, model_resp=False, DEBUG=True)


if __name__ == '__main__':
    wrapper()
