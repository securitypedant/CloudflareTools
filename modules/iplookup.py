import json
import logging
import logging.handlers as handlers

from requests import get

# logging.basicConfig(filename='ip_history.log', level=logging.INFO)
logger = logging.getLogger('ip_history')
logger.setLevel('INFO')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
logHandler = handlers.TimedRotatingFileHandler('ip_history.log', when='D', interval=1, backupCount=7)
logHandler.setLevel('INFO')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

def update_ip_history(ip_data):
    logger.info(f"{ip_data['query']}")

def get_last_ip_data():
    try:
        with open('ip_data.json', 'r') as f:
            last_entry = json.load(f)

    except FileNotFoundError:
        last_entry = None

    return last_entry 

def get_current_ip():
    data = get_ip_data()
    return data['query']

def get_ip_data():
    # Use https://ipapi.co/
    # FIXME: This API is free up to 1,000 lookups a month. Need to handle errors.
    # ip_data = get('https://ipapi.co/json/')
    ip_data_response = get('http://ip-api.com/json/')
    
    return json.loads(ip_data_response.content)
    