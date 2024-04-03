from flask import render_template
from modules.cloudflare import create_update_dns_record
from modules.iplookup import get_my_ip_data

def home():
    return render_template('home.html')

def test():
    ip_data = get_my_ip_data()
    create_update_dns_record('test.thorpevillage.com', ip_data['query'], 'A')

    return ip_data