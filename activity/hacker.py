import os
from dotenv import load_dotenv
from requests import get

# load environment file (.env)
load_dotenv()

BASE_URL = os.environ["HACKABLE_URL"]

# Single action example
response = get(f"{BASE_URL}/secrets", auth=("admin", "admin"))
if response.ok:
    print(f"Success!!!! Secrets: {response.text}")
