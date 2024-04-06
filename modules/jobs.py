import json

from datetime import datetime
from modules.iplookup import get_my_ip_data

def update_ip_data():
    ip_data = get_my_ip_data()
    ip_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open('ip_data.json', 'w') as f:
        json.dump(ip_data, f)

def check_ip_data():
    # Get the last entry in our IP data file
    try:
        with open('ip_data.json', 'r') as f:
            last_entry = json.load(f)

    except FileNotFoundError:
        last_entry = {}

    # Get IP data
    ip_result = get_my_ip_data()
    # Add extra data
    ip_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        ip_result['query']: ip_result
    }

    # Write to file if our IP has changed since the last check.
    with open('ip_data.json', 'w') as f:
        json.dump(ip_data, f)