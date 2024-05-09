"""Module containing all Ajax related functions."""

from flask import jsonify, request, current_app
from modules.services import toggle_service_status

def ajax_update_service_status():
    """Toggle the status of a job."""
    service_name = request.form['buttonName']
    status = toggle_service_status(current_app, service_name)
 
    response_data = {'enabled': status}

    return jsonify(response_data)