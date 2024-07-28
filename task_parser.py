#!/bin/env python3
import zmq
import random


def assign_tasks(user_count: int = 0, task_count: int = 0):
    assignment_list = []
    if user_count == 0:
        return list(0, 0)
    for user in user_count:
        index_assignment = random.randint(0, task_count)
        assignment_list.append(index_assignment)
    return assignment_list


def server(ip: str = 'localhost', port: int = 5557, DEBUG: bool = False):
    context = zmq.Context()
    svc_string = "**TASK SERVER"
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{ip}:{port}")
    print(f"{svc_string}: Connecting to tcp://{ip}:{port}")
    while True:
        #  Wait for request from client
        message = socket.recv().decode('utf-8')
        if DEBUG:
            print(f"{svc_string}: Received request: {message}")
        user_count = int(message.split(",")[0])
        task_count = int(message.split(",")[1])
        assignments = assign_tasks(user_count, task_count)
        # now make csv for ease of use
        assignments = str(assignments)[1:-1]
        assignments = assignments.replace(" ", "")
        if DEBUG:
            print(f"{svc_string}: parsed assignments into {assignments}")

        send_message = bytes(f"{assignments}", 'utf-8')

        new_message = f"{svc_string}: Replying - " + str(send_message[:10])
        print(f"{new_message}")

        #  Send reply back to client
        socket.send(send_message)
        print(f"{svc_string}: sent new message!")


context = zmq.Context()

def client(send_message: str, ip: str = 'localhost', port: int = 5557, DEBUG: bool = False):
    #  Socket to talk to server
    client_string = "**TASK CLIENT"
    print(f"{client_string}: Connecting to tcp://{ip}:{port}")
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{ip}:{port}")
    send_message = bytes(send_message, 'utf-8')
    # Send a message
    if DEBUG:
        print(f"{client_string}: Sending message '{send_message}'")
    socket.send(send_message)
    if DEBUG:
        print(f"{client_string}: waiting for response to request")
    #  Get the reply.
    message = socket.recv()
    if DEBUG:
        print(f"{client_string}: Received reply: {message}")

    return message


if __name__ == '__main__':
    server(DEBUG=True)
