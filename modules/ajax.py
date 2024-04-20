import json

from flask import jsonify, request, current_app
from modules.tools import get_service_status
from modules.jobs import update_job_status, get_jobid_by_name

def ajax_update_service_status():
    # Update whatever local service we want.
    service_name = request.form['buttonName']
    status, config = get_service_status(service_name)
    job_id = get_jobid_by_name(current_app.scheduler, service_name)

    update_job_status(job_id, status)


    with open('config.json', 'w') as f:
        json.dump(config_data, f)

    response_data = {'enabled': status}

    return jsonify(response_data)