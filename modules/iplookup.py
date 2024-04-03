import json

from requests import get

def get_my_ip_data():
    # Use https://ipapi.co/
    # FIXME: This API is free up to 1,000 lookups a month. Need to handle errors.
    # ip_data = get('https://ipapi.co/json/')
    ip_data_response = get('http://ip-api.com/json/')
    
    return json.loads(ip_data_response.content)
    