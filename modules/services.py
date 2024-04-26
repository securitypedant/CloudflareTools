import json
import modules.jobs

from flask import current_app

from datetime import datetime
from modules.iplookup import get_ip_data
from modules.tools import get_config, save_config

def get_service_status(service_name):
    # Return True if the service is enabled, False if not.
    try:
        config = get_config()
        service_status = config[service_name]['status']
    except:
        raise

    return service_status, config

def toggle_service_status(app, service_name):
    scheduler = app.scheduler

    config = get_config()
    job_id = get_jobid_by_name(scheduler, service_name)
    job = scheduler.get_job(job_id)

    # Is current status different?
    if config[service_name]['status']:
        job.pause()
        config[service_name]['status'] = False
    else:
        job.resume()
        config[service_name]['status'] = True

    save_config(config)
    
    return config[service_name]['status']
        
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
def reschedule_sync_job(app, jobname, new_interval_minutes):
    scheduler = app.scheduler

    job_id = get_jobid_by_name(scheduler, jobname)
    job = scheduler.get_job(job_id)    

    job.reschedule(trigger="interval", minutes=int(new_interval_minutes))

def get_jobid_by_name(scheduler, job_name):
    jobs = scheduler.get_jobs()

    for job in jobs:
        if job.name == job_name:
            return job.id
    return False

def initialize_jobs(app, scheduler):
    config = get_config()

    for job in config:
        scheduler.add_job(name=job, func=getattr(modules.jobs, job), trigger="interval", minutes=int(config[job]['sync_period']))
    
    app.scheduler = scheduler
    scheduler.start()
