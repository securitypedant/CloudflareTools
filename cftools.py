import atexit

from app import create_app
from modules.ux import home, test

from apscheduler.schedulers.background import BackgroundScheduler
from modules.jobs import update_ip_data

app = create_app()

# Routes
app.add_url_rule('/', view_func=home, methods=['GET', 'POST'])
app.add_url_rule('/test', view_func=test)

# Details on the Secret Key: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing the session data.
app.secret_key = 'BAD_SECRET_KEY_CHANGE_ME'

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_ip_data, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
