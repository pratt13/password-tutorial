from helpers import iter_test, single_post, multi_post
from task1_boyle import boyles_task

# Uncomment below lines when working on relevant task
# from task1_terry import terrys_task
# from task2 import generate_password

# Add the URL here you want to hack
# One time URL - change once
BASE_URL = "http://localhost:5000"

# Uncomment and recomment each task when required
iter_test(f"{BASE_URL}/task1/boyles_secret", "boyle", boyles_task)
# Maximum number of possible combos is 6 * 14 * 14 = 1176
# iter_test(f"{BASE_URL}/task1/terrys_secret", "terry", terrys_task, num_attempts=1176)
# single_post(f"{BASE_URL}/task2/level_one_a", generate_password)
# single_post(f"{BASE_URL}/task2/level_one_b", generate_password)
# single_post(f"{BASE_URL}/task2/level_one_c", generate_password)
# single_post(f"{BASE_URL}/task2/level_one_d",generate_password)
# single_post(f"{BASE_URL}/task2/level_one_e",generate_password)
# single_post(f"{BASE_URL}/task2/level_two", generate_password)
# single_post(f"{BASE_URL}/task2/level_three",generate_password)
# multi_post(f"{BASE_URL}/task2/level_four", generate_password)
# multi_post(f"{BASE_URL}/task2/level_five", generate_password)
