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
- run all microservices with the ui last
- like: 
    + terminal 1: `python3 openmeteo_icon_query.py`
    + terminal 2: `python3 meteo_blue_query.py`
    + terminal 3: `get_quote.py`
    + terminal 4: `task_parser.py`
    + terminal 5: `ui.py`

### microservice list:
+ CLI user interface
+ ICON weather forecast
+ MBLUE weather forecast
+ Person/task assignment generator
+ Inspirational quote (client only)