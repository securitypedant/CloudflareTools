import json
import logging
import logging.handlers as handlers

from flask import current_app

from datetime import datetime
from modules.iplookup import get_ip_data, get_last_ip_data, update_ip_history
from modules.cloudflare import update_dyndns_records

dyndns_logger = logging.getLogger('dyndns_history')
dyndns_logger.setLevel('INFO')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
dyndns_logHandler = handlers.TimedRotatingFileHandler('dyndns_history.log', when='D', interval=1, backupCount=7)
dyndns_logHandler.setLevel('INFO')
dyndns_logHandler.setFormatter(formatter)
dyndns_logger.addHandler(dyndns_logHandler)

def update_job_status(job_id, status):
    scheduler = current_app.scheduler
    job = scheduler.get_job(job_id)
    if not status:
        job.pause()
    else:
        job.resume()

def ddns_sync_job():
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
        
def initialize_jobs(app, scheduler, config):
    scheduler.add_job(name='ddns-sync', func=ddns_sync_job, trigger="interval", minutes=int(config['sync_time']))
    
    app.scheduler = scheduler
    scheduler.start()

def check_ip_data():
    # Get the last entry in our IP data file
    try:
        with open('ip_data.json', 'r') as f:
            last_entry = json.load(f)

    except FileNotFoundError:
        last_entry = {}

    # Get IP data
    ip_result = get_ip_data()
    # Add extra data
    ip_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        ip_result['query']: ip_result
    }

    # Write to file if our IP has changed since the last check.
    with open('ip_data.json', 'w') as f:
        json.dump(ip_data, f)

# Function to reschedule the job
def reschedule_sync_job(new_interval_minutes):
    with current_app.app_context():
        sync_job = current_app.sync_job
    sync_job.reschedule(trigger="interval", minutes=int(new_interval_minutes))

def get_jobid_by_name(scheduler, job_name):
    jobs = scheduler.get_jobs()

    for job in jobs:
        if job.name == job_name:
            return job.id
    return False