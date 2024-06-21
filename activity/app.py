import os, sys
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Unauthorized



current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path  .dirname(current_directory)
sys.path.append(parent_directory)


from task1.constants import MIN_ENTROPY
from task1.helpers import compute_exact_password_entropy, entropy_estimate, is_valid_password, test_is_valid_password
from task2.helpers import bad_password_generator, pin_number
from common.exceptions import InvalidPasswordException,InvalidUserForPage

app = Flask(__name__)
auth = HTTPBasicAuth()

PIN = next(pin_number())
PASSWORD = next(bad_password_generator())

users = {
    "boyle": generate_password_hash(PIN),
    "terry": generate_password_hash(PASSWORD),
    "admin": generate_password_hash("admin"),
}

LEVEL_ONE = "level_one"
LEVEL_TWO = "level_two"
LEVEL_THREE = "level_three"
LEVEL_FOUR = "level_four"
ADMIN = "admin"
LEVEL_FIVE = "level_five"

@auth.get_user_roles
def get_user_roles(user):
    """
    Warning: This is a hack - we may the user to a role
    We are not really using roles
    """
    if user == LEVEL_FOUR or user == LEVEL_FIVE:
        return ADMIN
    return user

@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    return str(e.description), 401

def level_one(password):
    try:
        is_valid_password(password, check_numbers=True, check_special_chars=True, check_uppercase=True)
    except InvalidPasswordException as e:
        raise Unauthorized(e)
    
def level_two(password):
    entropy_value = entropy_estimate(password)
    if entropy_value <= MIN_ENTROPY(password):
        raise Unauthorized(f"Entropy {entropy_value} is less than the minimum {MIN_ENTROPY}")
    
        
def level_three(password):
    entropy_value = compute_exact_password_entropy(password)
    if entropy_value <= MIN_ENTROPY(password):
        raise Unauthorized(f"Entropy {entropy_value} is less than the minimum {MIN_ENTROPY}")
@auth.verify_password
def verify_password(username, password):
    """
    Password verifier
    """
    if username in (LEVEL_FOUR, LEVEL_FIVE, ADMIN):
        print(f"Username is {username}")
        return username
    if username not in request.full_path:
        expected_user = request.full_path.strip("?").split("/")[-1]
        raise Unauthorized(f"Must use username {expected_user} to access {request.full_path}")
    if username == LEVEL_ONE:
        level_one(password)
    elif username == LEVEL_TWO:
        level_one(password)
        level_two(password)
    elif username == LEVEL_THREE:
        level_one(password)
        level_two(password)
        level_three(password)
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


@app.route("/task1/level_one")
@auth.login_required(role=LEVEL_ONE)
def level1():
    return "Well done for solving level 1!"

@app.route("/task1/level_two")
@auth.login_required(role=LEVEL_TWO)
def level2():
    return "Well done for solving level 2!"


@app.route("/task1/level_three")
@auth.login_required(role=LEVEL_THREE)
def level3():
    return "Well done for solving level3!"


@app.route("/task1/level_four")
@auth.login_required(role=LEVEL_FOUR)
def level4():
    passwords = request.params["passwords"]
    if len(passwords) < 100:
        return "Must pass at least 100 passwords to test", 401
    if len(passwords) != set(passwords):
        return "Cannot include repeats in the password creation", 401
    return "Well done for solving level4!"


@app.route("/task1/level_five")
@auth.login_required(role=LEVEL_FIVE)
def level5():
    """
    We should check distribution, but this is simple.
    Every type of char in the repeats must appear in a position
    """
    num_tries = 100
    passwords = request.params["passwords"]
    resorted_passwords = [
        "".join([passwords[i][j] for i in range(num_tries)]) for j in range(len(passwords[0]))
    ]
    print(passwords)
    # result = False
    # try:
    #     if all(
    #         is_valid_password(pwd, max_length=num_tries, min_length=num_tries)
    #         for pwd in resorted_passwords
    #     ):
    #         result = True
    # except ValueError:
    #     raise Unauthorized(
    #         f"Some characters never appear in a particular position after {num_tries} tries"
    #     )

    # return "Well done for solving level5!"

if __name__ == "__main__":
    app.run()
