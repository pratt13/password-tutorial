from requests import get, post

from task1.task1 import generate_password
from task2.task2 import pin_number_solver

# Add the URL here you want to hack
# One time URL - change once
BASE_URL = "http://localhost:5000"

def iter_test(url, generator, user):
    count = 0
    success = False
    solver = (guess for guess in generator())
    while count < 10**3:
        password = next(solver)
        response = get(f"{BASE_URL}/{url}", auth=(user, password))
        if response.ok:
            success = False
            break
        count +=1
    if success:
        print(f"Success!!!! Secrets: {response.text}")
        print(f"The pin number was {password}")
        print(f"Attempt: {count}")
    else:
        print(f"FAIL: Did not crack the password in {count} attempts")

def single_post(url, generator):
    response = post(f"{BASE_URL}/{url}", data={"password": generator()})
    if response.ok:
       print(f"Success!!!! Secrets: {response.text}")
    else:
        print(response.status_code)
        print(response.text)


def multi_post(url, generator):
    passwords = [generator() for _i in range(100)]
    print(passwords)
    response = post(f"{BASE_URL}/{url}", data={"passwords": passwords})

    if response.ok:
       print(f"Success!!!! Secrets: {response.text}")
    else:
        print(response.status_code)
        print(response.text)

# iter_test("task1/boyles_secret", "boyle",pin_number_solver )
# iter_test("task1/terrys_secret", "terry",pin_number_solver )
single_post("task2/level_one_a", generate_password)
single_post("task2/level_one_b", generate_password)
single_post("task2/level_one_c", generate_password)
single_post("task2/level_one_d",generate_password)
single_post("task2/level_one_e",generate_password)
single_post("task2/level_two", generate_password)
single_post("task2/level_three",generate_password)
multi_post("task2/level_four", generate_password)
multi_post("task2/level_five", generate_password)