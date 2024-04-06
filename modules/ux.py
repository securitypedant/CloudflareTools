import json

from flask import render_template
from modules.cloudflare import create_update_dns_record
from modules.iplookup import get_my_ip_data
from modules.jobs import update_ip_data

def home():
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
        dns_config = {}

    return render_template('home.html', current_ip_data=current_ip_data, dns_config=dns_config)

def test():
    update_ip_data()
    # create_update_dns_record('test.thorpevillage.com', ip_data['query'], 'A')

    return "Success"