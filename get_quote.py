#!/bin/env python3
import zmq
import random

quotes = [
    "Life is what happens when you're busy making other plans. - John Lennon",
    "Get busy living or get busy dying. - Stephen King",
    "You only live once, but if you do it right, once is enough. - Mae West",
    "Many of life's failures are people who did not realize how close they were to success when they gave up. - Thomas A. Edison",
    "If you want to live a happy life, tie it to a goal, not to people or things. - Albert Einstein",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.",
    "The best way to predict the future is to invent it. - Alan Kay",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "You miss 100% of the shots you don’t take. - Wayne Gretzky",
    "The purpose of our lives is to be happy. - Dalai Lama",
    "The only impossible journey is the one you never begin. - Tony Robbins",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "Believe you can and you’re halfway there. - Theodore Roosevelt",
    "Life is short, and it is up to you to make it sweet. - Sarah Louise Delany",
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "The journey of a thousand miles begins with one step. - Lao Tzu",
    "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. - Ralph Waldo Emerson",
    "You must be the change you wish to see in the world. - Mahatma Gandhi",
    "Happiness is not something ready made. It comes from your own actions. - Dalai Lama",
    "Life isn’t about finding yourself. Life is about creating yourself. - George Bernard Shaw",
    "The best revenge is massive success. - Frank Sinatra",
    "Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
    "Don’t watch the clock; do what it does. Keep going. - Sam Levenson",
    "Your time is limited, don’t waste it living someone else’s life. - Steve Jobs",
    "In three words I can sum up everything I’ve learned about life: it goes on. - Robert Frost",
    "You only live once, but if you do it right, once is enough. - Mae West",
    "The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
    "Everything you’ve ever wanted is on the other side of fear. - George Addair",
    "Opportunities don't happen. You create them. - Chris Grosser",
    "Dream big and dare to fail. - Norman Vaughan",
    "Our lives are defined by opportunities, even the ones we miss. - F. Scott Fitzgerald",
    "Act as if what you do makes a difference. It does. - William James",
    "Success is not how high you have climbed, but how you make a positive difference to the world. - Roy T. Bennett",
    "Life is either a daring adventure or nothing at all. - Helen Keller",
    "The harder you work for something, the greater you’ll feel when you achieve it. - Unknown",
    "Dream it. Believe it. Build it. - Unknown",
    "Don’t be pushed around by the fears in your mind. Be led by the dreams in your heart. - Roy T. Bennett",
    "The only way to achieve the impossible is to believe it is possible. - Charles Kingsleigh",
    "To accomplish great things, we must not only act, but also dream; not only plan, but also believe. - Anatole France",
    "The mind is everything. What you think you become. - Buddha",
    "The best way out is always through. - Robert Frost",
    "Your life does not get better by chance, it gets better by change. - Jim Rohn",
    "We may encounter many defeats but we must not be defeated. - Maya Angelou",
    "The only thing standing between you and your goal is the story you keep telling yourself as to why you can’t achieve it. - Jordan Belfort",
    "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
    "Everything you can imagine is real. - Pablo Picasso",
    "If you want to lift yourself up, lift up someone else. - Booker T. Washington",
    "Don’t be afraid to give up the good to go for the great. - John D. Rockefeller",
    "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
    "We are what we repeatedly do. Excellence, then, is not an act, but a habit. - Aristotle",
    "Life isn’t about waiting for the storm to pass, it’s about learning how to dance in the rain. - Vivian Greene",
    "If you’re going through hell, keep going. - Winston Churchill",
    "Keep your face always toward the sunshine—and shadows will fall behind you. - Walt Whitman",
    "The only person you should try to be better than is the person you were yesterday. - Unknown",
    "It always seems impossible until it’s done. - Nelson Mandela",
    "Start where you are. Use what you have. Do what you can. - Arthur Ashe",
    "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. - Christian D. Larson",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "Don’t be afraid to give up the good to go for the great. - John D. Rockefeller",
    "Our greatest glory is not in never falling, but in rising every time we fall. - Confucius",
    "Success is not how high you have climbed, but how you make a positive difference to the world. - Roy T. Bennett",
    "You don’t have to be great to start, but you have to start to be great. - Zig Ziglar",
    "What you get by achieving your goals is not as important as what you become by achieving your goals. - Zig Ziglar",
    "The harder the conflict, the greater the triumph. - George Washington",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us. - Ralph Waldo Emerson",
    "You don’t have to be great to start, but you have to start to be great. - Zig Ziglar",
    "It’s not whether you get knocked down, it’s whether you get up. - Vince Lombardi",
    "The only way to achieve the impossible is to believe it is possible. - Charles Kingsleigh",
    "The best way to predict the future is to create it. - Peter Drucker",
    "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
    "You can’t go back and change the beginning, but you can start where you are and change the ending. - C.S. Lewis",
    "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    "Success is walking from failure to failure with no loss of enthusiasm. - Winston Churchill",
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "Happiness is not something ready made. It comes from your own actions. - Dalai Lama",
    "The only person you should try to be better than is the person you were yesterday. - Unknown",
    "You can’t go back and change the beginning, but you can start where you are and change the ending. - C.S. Lewis",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "Do what you can, with what you have, where you are. - Theodore Roosevelt",
    "You must do the things you think you cannot do. - Eleanor Roosevelt",
    "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    "If you want to achieve greatness stop asking for permission. - Anonymous",
    "Believe you can and you’re halfway there. - Theodore Roosevelt",
    "The best way out is always through. - Robert Frost",
    "Don’t count the days, make the days count. - Muhammad Ali",
    "Your life is your message to the world. Make it inspiring. - Unknown",
    "Act as if what you do makes a difference. It does. - William James",
    "Success is not how high you have climbed, but how you make a positive difference to the world. - Roy T. Bennett"]

def server(ip: str = 'localhost', port: int = 5558, DEBUG: bool = False):
    print("!! Initializing the QUOTE SERVER !!")
    context = zmq.Context()
    svc_string = "**QUOTE SERVER"
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{ip}:{port}")
    print(f"{svc_string}: Connecting to tcp://{ip}:{port}")

    while True:
        # wait for request from client
        message = socket.recv().decode('utf-8')
        if DEBUG:
            print(f"{svc_string}: Received request: {message}")

        # select a random quote from the list
        selected_quote = random.choice(quotes)

        # convert the selected quote to bytes
        send_message = bytes(selected_quote, 'utf-8')
        if DEBUG:
            print(f"{svc_string}: Replying with quote: {selected_quote}")
        # send reply back to client
        socket.send(send_message)



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
