#!/bin/env python3
import zmq
import random


def assign_tasks(user_count: int = 0, task_count: int = 0, DEBUG: bool = False):
    assignment_list = []
    if user_count == 0:
        assignment_list = [ 0, ]
        return assignment_list
    for user in range(user_count):
        index_assignment = random.randint(0,task_count)
        if DEBUG:
            print(f"**Assign Tasks: user={str(user)}, random_task={str(index_assignment)}")
        assignment_list.append(index_assignment)
    if DEBUG:
        print(f"**Assign Tasks: finalized assignment_list as {str(assignment_list)}")
    return assignment_list


def server(ip: str = 'localhost', port: int = 5557, DEBUG: bool = False):
    print("!! Initializing the TASK SERVER !!")
    context = zmq.Context()
    svc_string = "**TASK SERVER"
    socket = context.socket(zmq.REP)
    socket.setsockopt(zmq.LINGER, 100)
    socket.bind(f"tcp://{ip}:{port}")
    print(f"{svc_string}: Connecting to tcp://{ip}:{port}")
    while True:
        #  Wait for request from client
        try:
            message = socket.recv(copy=True).decode('utf-8')
            if DEBUG:
                print(f"{svc_string}: Received request: {message}")
            if "," not in str(message):
                print(f"{svc_string}: Incorrectly formatted request received, missing the ',' separator.")
            user_count = int(message.split(",")[0])
            task_count = int(message.split(",")[1])
        except Exception as err:
            formatted_err = str(err).strip()
            formatted_err = formatted_err.replace("\n", "")
            print(f"{svc_string}: unable to complete user / task assignment due to error {formatted_err}")
            socket.close()
            server(ip=ip, port=port, DEBUG=DEBUG)
            break
        assignments = assign_tasks(user_count, task_count, DEBUG=DEBUG)
        # now make comma separated for ease of use
        assignments = str(assignments)[1:-1]
        assignments = assignments.replace(" ", "")
        if DEBUG:
            print(f"{svc_string}: parsed assignments into {assignments}")
        # convert the message to bytes
        send_message = bytes(f"{assignments}", 'utf-8')
        new_message = f"{svc_string}: Replying - " + str(send_message)[:10] + "..."
        if DEBUG:
            print(f"{new_message}")
        #  Send reply back to client
        socket.send(send_message)
        print(f"{svc_string}: sent a message!")


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
    message = str(message.decode('utf-8'))
    # format the message into an array / list
    message = message.split(",")
    if DEBUG:
        print(f"{client_string}: received message {str(message)}")
    return message


if __name__ == '__main__':
    server(ip='localhost', DEBUG=True)
    #client(send_message='0,0', DEBUG=True)