import atexit
import json

from app import create_app
from modules.ux import home, test, ddns_ux

from apscheduler.schedulers.background import BackgroundScheduler
from modules.jobs import initialize_jobs
from modules.ajax import ajax_update_service_status

from flask import current_app

app = create_app()

# Routes
app.add_url_rule('/', view_func=home, methods=['GET', 'POST'])
app.add_url_rule('/ddns', view_func=ddns_ux, methods=['GET', 'POST'])

app.add_url_rule('/ajax/update_service_status', view_func=ajax_update_service_status, methods=['POST'])
app.add_url_rule('/test', view_func=test)

# Details on the Secret Key: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing the session data.
app.secret_key = 'BAD_SECRET_KEY_CHANGE_ME'

# TODO: Check this is the best way to do this.
def json_query_filter(json_string, key):
    data = json.loads(json_string)
    return data.get(key)

app.jinja_env.filters['json_query'] = json_query_filter

# Get current sync timeframe if it exists.
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except:
    config = {
        "sync_time": 60
    }

scheduler = BackgroundScheduler()
initialize_jobs(app, scheduler, config)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
