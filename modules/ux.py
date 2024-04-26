import json
from datetime import datetime

from flask import render_template, request, redirect, url_for, current_app
from modules.cloudflare import get_zones, get_existing_dyndns_records, create_update_dns_record, delete_dns_record
from modules.services import reschedule_sync_job
from modules.iplookup import get_current_ip
from modules.tools import parse_log_file_to_array, get_config
from modules.jobs import ddns_sync

def home():
    return render_template(
        'home.html',
        config=get_config()
        )

def ddns_ux():
    if request.method == 'POST':
        # Deal with a form post form the home page.
        if 'add-button' in request.form:
            hostname = request.form.get('hostname')
            domain = request.form.get('domain-select')
            utc_now = datetime.utcnow()
            utc_seconds = int(utc_now.timestamp())

            create_update_dns_record(fqdn=f'{hostname}.{domain}', 
                                     ip=get_current_ip(),
                                     comment=f'DynDNS: Entry managed by CloudflareTools. Last update: {utc_seconds}',
                                     type='A'
                                     )
        elif 'update-ipdata-button' in request.form:
            ddns_sync()

        elif 'delete-button' in request.form:
            # Delete the DNS entry.
            hostname = request.form.get('delete-hostname')
            hostparts = hostname.split(".")
            domain_name = ".".join(hostparts[1:])

            zone_id = request.form.get('delete-zone-id')
            delete_dns_record(zone_id, domain_name)
        
        elif 'update-frequency-button' in request.form:
            frequency = request.form.get('frequency')
            
            with open('config.json', 'r') as file:
                config_data = json.load(file)

            config_data['ddns_sync']['sync_period'] = frequency

            with open('config.json', 'w') as f:
                json.dump(config_data, f, indent=4)

            # Update the job timeframe.
            reschedule_sync_job(current_app, 'ddns_sync', frequency)

        return redirect(url_for('ddns_ux'))


    # Open the latest information about the internet config.
    try:
        with open('ip_data.json', 'r') as f:
            current_ip_data = json.load(f)

    except FileNotFoundError:
        current_ip_data = {}

    # Open the ip history log.
    try:
        with open('ip_history.log', 'r') as f:
            ip_history = parse_log_file_to_array(f)
    except:
        ip_history = None

    # Open the DynDNS history log.
    try:
        with open('dyndns_history.log', 'r') as f:
            dyndns_history = parse_log_file_to_array(f)
    except:
        dyndns_history = None

    # Open the current DynDns config.
    with open('config.json', 'r') as f:
        config = json.load(f)

    zones = get_zones()
    existing_dyndns_entries = get_existing_dyndns_records()
    zone_names = [zone.name for zone in zones]

    return render_template('dyndns.html', 
                           current_ip_data=current_ip_data, 
                           config=config,
                           zone_names=zone_names,
                           existing_dyndns_entries=existing_dyndns_entries,
                           ip_history=ip_history,
                           dyndns_history=dyndns_history
                           )