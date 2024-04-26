import os
import sys
import json

from flask import Flask

from modules.jobs import ddns_sync

def create_app():
    app = Flask(__name__)
    env_cf_api_token = os.environ.get('CF_API_TOKEN')

    # Check if the environment variable exists and is not an empty string
    if env_cf_api_token and env_cf_api_token.strip():
        # Set the configuration variable in Flask
        app.config['CF_API_TOKEN'] = env_cf_api_token
    else:
        # We don't have an API token set.
        print("Environment variable for API token is not set.")
        print("Please set CF_API_TOKEN with an API token.")
        sys.exit(1)

    if not os.path.exists('ip_data.json'):
        ddns_sync()

    if not os.path.exists('config.json'):
        # If no config exists, create one.
        default_config = {
                            "ddns_sync": {"status": False, "sync_period": 360, "name": "ddns_sync", "title": "Dynamic DNS", "desc": "Dynamic DNS sync", "stub_func": "ddns_ux"}
                          }

        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=4)
    
    return app

