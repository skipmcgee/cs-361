# cs-361
cli client for the cs-361 class
implements microservices
uses zeromq to communicate between them

### setup instructions
+ `python3 -m venv venv`
+ `source venv/bin/activate` (platform dependent)
+ `python3 -m pip install -r requirements.txt`
+ add your free meteo blue token to a .env file using the variable name "meteo_blue_token"

### useage instructions
- run each file in a terminal as a microservice
- defaults should work for all servers
- like: `python3 ui.py`
