import os, sys, json
from flask import Flask, jsonify, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Unauthorized


current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)



from task1.constants import MIN_ENTROPY
from task1.helpers import (
    compute_exact_password_entropy,
    entropy_estimate,
    is_valid_password,
)
from task2.helpers import bad_password_generator, pin_number
from common.exceptions import InvalidPasswordException

app = Flask(__name__)
auth = HTTPBasicAuth()

PIN = next(pin_number())
PASSWORD = next(bad_password_generator())
ADMIN_PASSWORD = "admin"
users = {
    "boyle": generate_password_hash(PIN),
    "terry": generate_password_hash(PASSWORD),
    "admin": generate_password_hash(ADMIN_PASSWORD),
}

ADMIN = "admin"
LEVEL_ONE = "level_one"
LEVEL_TWO = "level_two"
LEVEL_THREE = "level_three"
LEVEL_FOUR = "level_four"
LEVEL_FIVE = "level_five"
TERRY = "terry"
BOYLE = "boyle"


@auth.get_user_roles
def get_user_roles(user):
    """
    Warning: This is a hack - we may the user to a role
    We are not really using roles
    """
    return user


@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    """
    Do not return a HTML template for errors to allow processing
    """
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
        "failed_url": request.url,
    })
    response.content_type = "application/json"
    return response


def level_one(
    password, check_numbers=True, check_special_chars=True, check_uppercase=True, check_sub_set=True
):
    try:
        is_valid_password(
            password,
            check_numbers=check_numbers,
            check_special_chars=check_special_chars,
            check_uppercase=check_uppercase,
            check_sub_set=check_sub_set,
        )
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


def level_four(passwords):
    if len(passwords) < 100:
        return "Must pass at least 100 passwords to test", 401
    if len(passwords) != set(passwords):
        return "Cannot include repeats in the password creation", 401


@auth.verify_password
def verify_password(username, password):
    """
    Password verifier
    """
    if username == ADMIN:
        return username
    if username not in request.full_path:
        expected_user = request.full_path.strip("?").split("/")[-1]
        raise Unauthorized(f"Must use username {expected_user} to access {request.full_path}")
    if username in users and check_password_hash(users.get(username), password):
        return username
    # In the browser we want a login
    # From python we want it passed via the request
    # If we wanted to handle this with curl we would do the negative
    if "python-requests" in request.headers.get("User-agent"):
        raise Unauthorized(f"Invalid credentials to access {request.full_path}")


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/info/characters")
def characters():
    return render_template("characters.html")


@app.route("/info/entropy")
def entropy():
    return render_template("entropy.html")


@app.route("/info/randomness")
def randomness():
    return render_template("randomness.html")

@app.route("/task1/info")
def task1():
    return render_template("task1/info.html", root_url=request.root_path)


@app.route("/task1/help_boyle")
def task1_help_boyle():
    return render_template("task1/help_boyle.html")


@app.route("/task1/help_terry")
def task1_help_terry():
    return render_template("task1/help_terry.html")


@app.route("/task1/boyles_secret")
@auth.login_required(role=[BOYLE, ADMIN])
def secrets_boyle():
    if auth.current_user() == BOYLE:
        return f"Well done for guessing the password for user `{auth.current_user()}` - too simple to guess {PIN}. The secret is `Desperate times call for Desperate Housewives`!"
    return "Sneaky you got the admin password."


@app.route("/task1/terrys_secret")
@auth.login_required(role=[BOYLE, ADMIN])
def secrets_terry():
    if auth.current_user() == TERRY:
        return f"Well done for guessing the password for user `{auth.current_user()}` - too simple to guess {PASSWORD}. The secret is `Terry loves yoghurt`!"
    return "Sneaky you got the admin password."


@app.route("/task2/info")
def task2():
    return render_template("task2/info.html")


@app.route("/task2/help")
def task2_help():
    return render_template("task2/help.html")

@app.route("/task2/help2")
def task2_help2():
    return render_template("task2/help2.html")


@app.route("/task2/level_one_a", methods=["GET", "POST"])
def level1a():
    if request.method == "GET":
        return render_template("task2/input.html", info="Level 1a - enter an 8 character password")

    elif request.method == "POST":
        password = request.form.get("password", [])
        level_one(
            password,
            check_numbers=False,
            check_special_chars=False,
            check_uppercase=False,
            check_sub_set=False,
        )
        return render_template("success.html", message="Well done for solving level 1a!", next_task="level1b")


@app.route("/task2/level_one_b", methods=["GET", "POST"])
def level1b():
    if request.method == "GET":
        return render_template("task2/input.html", info="Level 1b - enter an 8 character password with a number")

    elif request.method == "POST":
        password = request.form.get("password", [])
        level_one(password, check_special_chars=False, check_uppercase=False, check_sub_set=False)
        return render_template("success.html", message="Well done for solving level 1b!", next_task="level1c")



@app.route("/task2/level_one_c", methods=["GET", "POST"])
def level1c():
    if request.method == "GET":
        return render_template("task2/input.html", info="Level 1c - enter an 8 character password with a number and capital letter")

    elif request.method == "POST":
        password = request.form.get("password", [])
        level_one(password, check_special_chars=False, check_sub_set=False)
        return render_template("success.html", message="Well done for solving level 1c!", next_task="level1d")



@app.route("/task2/level_one_d", methods=["GET", "POST"])
def level1d():
    if request.method == "GET":
        return render_template("task2/input.html", info="Level 1d - enter an 8 character password with a number, capital letter and special character.")

    elif request.method == "POST":
        password = request.form.get("password", [])
        level_one(password, check_sub_set=False)
        return render_template("success.html", message="Well done for solving level 1d!", next_task="level1e")



@app.route("/task2/level_one_e", methods=["GET", "POST"])
def level1e():
    if request.method == "GET":
        return render_template("task2/input.html", info="Level 1e - enter an 8 character password with a number, capital letter, special character and no common patterns.")

    elif request.method == "POST":
        password = request.form.get("password", [])
        level_one(password)
        return render_template("success.html", message="Well done for solving level 1e!", next_task="level2")


@app.route("/task2/level_two", methods=["GET", "POST"])
def level2():
    if request.method == "GET":
        return render_template("task2/input.html", info="Level 2 - enter a password that has an expected high complexity")

    elif request.method == "POST":
        password = request.form.get("password")
        level_one(password)
        level_two(password)
        return render_template("success.html", message="Well done for solving level 2!", next_task="level3")



@app.route("/task2/level_three", methods=["GET", "POST"])
def level3():
    if request.method == "GET":
        return render_template("task2/input.html", info="Level 3 - enter a password that has a high complexity")
    
    elif request.method == "POST":
        password = request.form.get("password")
        level_one(password)
        level_two(password)
        level_three(password)
        return render_template("success.html", message="Well done for solving level 3!", next_task="level4")


@app.route("/task2/level_four")
def level4():
    passwords = request.params["passwords"]
    for password in passwords:
        level_one(password)
        level_two(password)
        level_three(password)
    level_four(passwords)
    return render_template("success.html", message="Well done for solving level 2!", next_task=None)


@app.route("/task2/level_five")
def level5():
    """
    We should check distribution, but this is simple.
    Every type of char in the repeats must appear in a position.
    Reshape the array, so each element in the array represents the
     position, for example, the 6th element is a combination of all the
      characters that appear in the 6th position. is in the
    """
    passwords = request.args.getlist("passwords")

    # Check all passwords are valid
    for password in passwords:
        level_one(password)
        level_two(password)
        level_three(password)
    # Check level 4
    level_four(passwords)

    # Now level 5
    all_chars_present = set([char for password in passwords for char in password])
    num_tries = len(passwords)

    resorted_passwords = [
        "".join([passwords[i][j] for i in range(num_tries)]) for j in range(len(passwords[0]))
    ]
    for resorted_password in resorted_passwords:
        if (all_chars_present & set(resorted_password)) != 0:
            return Unauthorized("Some characters don't appear in all positions"), 401

    return "Well done for solving level5!"


if __name__ == "__main__":
    app.run()
