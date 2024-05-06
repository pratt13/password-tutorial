import os, sys
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)


from task2.helpers import bad_password_generator, pin_number

app = Flask(__name__)
auth = HTTPBasicAuth()

PIN = next(pin_number())
PASSWORD = next(bad_password_generator())

users = {
    "boyle": generate_password_hash(PIN),
    "terry": generate_password_hash(PASSWORD),
    "admin": generate_password_hash("admin"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route("/")
def index():
    return "Hello, all my secrets are stored in /secrets url, with username `boyle` and/or `terry`. Can you get to them?"


@app.route("/help")
def help():
    return "Try accessing `/secrets` via the browser.\nNext try using it via curl -u <username>:<password> localhost:5000/secrets"


@app.route("/secrets")
@auth.login_required
def secrets():
    if auth.current_user() == "boyle":
        return f"Well done for guessing the password for user `{auth.current_user()}` - too simple to guess {PIN}. The secret is `Desperate times call for Desperate Housewives`!"
    elif auth.current_user() == "terry":
        return f"Well done for guessing the password for user `{auth.current_user()}` - too simple to guess {PASSWORD}. The secret is `Terry loves yoghurt`!"
    elif auth.current_user() == "admin":
        return "Sneaky you got the admin password."
    return "Who is this?"


if __name__ == "__main__":
    app.run()
