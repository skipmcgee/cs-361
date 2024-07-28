#!/bin/env python3
import zmq


"""
def server(ip: str = 'localhost', port: int = 5558, DEBUG: bool = False):
    print("!! Initializing the QUOTE SERVER !!")
    context = zmq.Context()
    svc_string = "**QUOTE SERVER"
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{ip}:{port}")
    print(f"{svc_string}: Connecting to tcp://{ip}:{port}")
    while True:
        #  Wait for request from client
        message = socket.recv().decode('utf-8')
        if DEBUG:
            print(f"{svc_string}: Received request: {message}")

    
        # **** add your server logic here ****

        
        # convert the message to bytes
        send_message = bytes(f"{assignments}", 'utf-8')
        new_message = f"{svc_string}: Replying - " + str(send_message[:10])
        if DEBUG:
            print(f"{new_message}")
        #  Send reply back to client
        socket.send(send_message)
        print(f"{svc_string}: sent new message!")
    """

context = zmq.Context()

def client(send_message: str, ip: str = 'localhost', port: int = 5558, DEBUG: bool = False):
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
    message = str(message)
    # format the message into an array / list
    # start by removing bytes conversion stuffs
    message = message[2:-1]
    if DEBUG:
        print(f"{client_string}: formatted message into type {type(message)} as: {str(message)}")
    return message


if __name__ == '__main__':
    client(send_message='Please quote me', DEBUG=True)
