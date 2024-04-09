import atexit
import json

from app import create_app
from modules.ux import home, test

from apscheduler.schedulers.background import BackgroundScheduler
from modules.jobs import update_ip_data

from flask import current_app

app = create_app()

# Routes
app.add_url_rule('/', view_func=home, methods=['GET', 'POST'])
app.add_url_rule('/test', view_func=test)

# Details on the Secret Key: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing the session data.
app.secret_key = 'BAD_SECRET_KEY_CHANGE_ME'

# Get current sync timeframe if it exists.
try:
    with open('dns_config.json', 'r') as f:
        dns_config = json.load(f)
except:
    dns_config = {
        "sync_time": 60
    }

scheduler = BackgroundScheduler()
sync_job = scheduler.add_job(func=update_ip_data, trigger="interval", minutes=int(dns_config['sync_time']))
with app.app_context():
        current_app.sync_job = sync_job
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
