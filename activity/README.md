# Flask Example

## Setup
Create the environment and run the app.
```sh
python3 -m venv flask-app
source flask-app/bin/activate
pip3 install -r requirements.txt
flask run --host=0.0.0.0
```

## Hack the app

### Bash terminal via curl

```sh
curl -u boyle:<password> localhost:5000/secrets
curl -u terry:<password> localhost:5000/secrets
curl -X POST localhost:5000/task2/level_one_b  -o /dev/null -s -w "%{http_code}\n" --data '{"password":"2ss":}'
```

### Python
Look at the hacker.py file amd modify it to try and hack the password.
Currently it does it once, you need to try multiple passwords (lots).
Use one of the exercises from earlier.

```sh
source flask-app/bin/activate
python3 hacker.py
```