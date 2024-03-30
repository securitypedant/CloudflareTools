from flask import Flask

from lib.ux import home, test

app = Flask(__name__)
# Details on the Secret Key: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing the session data.
app.secret_key = 'BAD_SECRET_KEY_CHANGE_ME'

# Routes
app.add_url_rule('/', view_func=home)
app.add_url_rule('/test', view_func=test)

if __name__ == "__main__":
    app.run()
