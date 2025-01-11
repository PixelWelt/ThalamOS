import requests

import os
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), 'data/.env')
load_dotenv(dotenv_path=ENV_PATH)

SCALE_HOST = os.getenv("SCALE_HOST")
print(f'WifiScale host is: {SCALE_HOST}')


def get_weight():
    """
    Retrieve the weight of the scale.
    This function sends a GET request to the specified API endpoint to retrieve the weight of the scale.
    Returns:
        float: The weight of the scale.
    """
    API = f"http://{SCALE_HOST}/getWeight"
    response = requests.get(API)
    weight = response.content.decode('utf-8')
    return weight
