import json

from flask import render_template, request
from modules.cloudflare import get_zones, get_existing_dyndns_records, create_update_dns_record, delete_dns_record
from modules.jobs import update_ip_data
from modules.iplookup import get_current_ip

def home():
    if request.method == 'POST':
        # Deal with a form post form the home page.
        if 'add-button' in request.form:
            hostname = request.form.get('hostname')
            domain = request.form.get('domain-select')

            create_update_dns_record(fqdn=f'{hostname}.{domain}', 
                                     ip=get_current_ip(),
                                     comment='DynDNS: Entry managed by CloudflareTools.',
                                     type='A'
                                     )
        elif 'delete-button' in request.form:
            # Delete the DNS entry.
            hostname = request.form.get('delete-hostname')
            hostparts = hostname.split(".")
            domain_name = ".".join(hostparts[1:])

            zone_id = request.form.get('delete-zone-id')
            delete_dns_record(zone_id, domain_name)

    # Open the latest information about the internet config.
    try:
        with open('ip_data.json', 'r') as f:
            current_ip_data = json.load(f)

    except FileNotFoundError:
        current_ip_data = {}

    # Open the current DynDns config.
    try:
        with open('dns_config.json', 'r') as f:
            dns_config = json.load(f)
    except:
        dns_config = None

    zones = get_zones()
    existing_dyndns_entries = get_existing_dyndns_records()
    zone_names = [zone.name for zone in zones]

    return render_template('home.html', 
                           current_ip_data=current_ip_data, 
                           dns_config=dns_config,
                           zone_names=zone_names,
                           existing_dyndns_entries=existing_dyndns_entries
                           )

def test():
    update_ip_data()
    # create_update_dns_record('test.thorpevillage.com', ip_data['query'], 'A')

    return "Success"