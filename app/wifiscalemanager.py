"""
wifiscalemanager.py

This module provides functionality to interact with a WiFi-enabled scale. 
It retrieves the weight from the scale by sending a GET request to the specified API endpoint.

Functions:
    get_weight(): Retrieves the weight of the scale.

Environment Variables:
    SCALE_HOST: The hostname or IP address of the WiFi scale, loaded from a .env file.

Dependencies:
    - requests: To send HTTP requests.
    - os: To handle file paths and environment variables.
    - dotenv: To load environment variables from a .env file.
"""
import os
from typing import Annotated
import requests
from dotenv import load_dotenv


ENV_PATH: Annotated[str, "path to environment variables"] = os.path.join(os.path.dirname(__file__), 'data/.env')
load_dotenv(dotenv_path=ENV_PATH)

SCALE_HOST: Annotated[str, "environment variable for wifi scale address"] = os.getenv("SCALE_HOST")
print(f'WifiScale host is: {SCALE_HOST}')


def get_weight() -> Annotated[float, "weight in grams"]:
    """
    Retrieve the weight of the scale.
    This function sends a GET request to the specified API endpoint
    to retrieve the weight of the scale.
    Returns:
        float: The weight of the scale.
    """
    api = f"http://{SCALE_HOST}/getWeight"
    try:
        response = requests.get(api, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving weight: {e}")
        return "ERROR SCALE NOT FOUND"
    weight = response.content.decode('utf-8')
    return weight
