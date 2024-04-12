import os
import sys

from flask import Flask

from modules.jobs import update_ip_data

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
        update_ip_data()

    return app

