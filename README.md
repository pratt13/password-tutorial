# Password Hacking

How safe is your password?
What is a strong password?

This repository is a simple python repository to demonstrate how to:
a. Crack bad passwords using 2 obvious techniques.
b. Generate a strong(ish) password in python

## Setup
This can be run in two different ways.

### Locally

#### Run the flask app
```sh
cd activity
python3 -m venv flask-app
source flask-app/bin/activate
pip3 install -r requirements.txt
flask run --host=0.0.0.0
```

#### The tasks
Change the BASE_URL in `main.py`.
Run,
```sh
python3 main.py
```


## Tasks
Summary of tasks are below, but the flask app has far more information of you navigate to it.
Locally, if run it will be on `localhost:5000` or on replit it will be the URL given.
### Task 1
#### Boyle's Task

Boyle has a web page with all his secrets, he has a password as a three digit pin. Can you guess it?

#### Terry's Task

Terry has a web page with all his secrets, he has a password that uses four common phrases, plus two extra characters.

## Task 2
Create a python function to generate a password of 8 characters.
It must have:
* A lowercase letter
* An uppercase letter
* A number
* A special character `£$?!_`
* No examples of `Qwerty, Password, Pa$$w0rd, yoghurt, cagney, lacey`
* No repeats within 100 tries
* Range of characters, not all the letter `a1a2a3a4`
* All characters are randomly and uniformly chosen.

## Testing
### Unit tests

```sh
python3 -m unittest
```
