import json
import logging
import logging.handlers as handlers

from modules.cf import update_dyndns_records
from datetime import datetime
from modules.iplookup import get_ip_data, get_last_ip_data, update_ip_history

dyndns_logger = logging.getLogger('dyndns_history')
dyndns_logger.setLevel('INFO')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
dyndns_logHandler = handlers.TimedRotatingFileHandler('dyndns_history.log', when='D', interval=1, backupCount=7)
dyndns_logHandler.setLevel('INFO')
dyndns_logHandler.setFormatter(formatter)
dyndns_logger.addHandler(dyndns_logHandler)

def ddns_sync():
    ip_data = get_ip_data()
    ip_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    last_ip_data = get_last_ip_data()

    # Only update our record if the current IP is different to the last one.
    if last_ip_data:
        if last_ip_data['query'] != ip_data['query']:
            with open('ip_data.json', 'w') as f:
                json.dump(ip_data, f)
            
            # Update all our DynDNS records.
            update_dyndns_records(ip_data['query'])

            # Add to the history of changes
            update_ip_history(ip_data)
            dyndns_logger.info(f"IP changed. From {last_ip_data['query']} to {ip_data['query']}")
        else:
            dyndns_logger.info(f"IP not changed. {ip_data['query']}")
    else:   
        with open('ip_data.json', 'w') as f:
            json.dump(ip_data, f)