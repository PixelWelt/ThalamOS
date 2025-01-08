import requests
import json
import os
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), 'data/.env')
load_dotenv(dotenv_path=ENV_PATH)

WLED_HOST = os.getenv("WLED_HOST")
print(f'WLED host is: {WLED_HOST}')

API = f"http://{WLED_HOST}/json"


def turnOffLights():
    """
    Sends a request to turn off the lights by setting the segment color to black.
    This function creates a JSON payload to set the color of a segment of lights to black (hex code "000000")
    and sends a POST request to the specified API endpoint to turn off the lights.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    req = json.dumps({"seg":{"i":[0,50,"000000"]}})
    requests.post(API, req)


def colorPos(pos):
    """
    Sends a request to set the color of a specific position on a WLED device.
    Args:
        pos (int): The position to set the color for.
    Returns:
        None
    """
    req = json.dumps({"seg":{"i":[pos, "FF0000"]}})
    requests.post(API, req)


def loadDefaultState():
    """
    Sends a POST request to the WLED API to load the default state.
    This function creates a JSON payload with a preset state identifier and sends it to the WLED API endpoint using a POST request.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    req = json.dumps({"ps":1})
    requests.post(API, req)


def changePowerState(state):
    """
    Change the power state of the device.
    Args:
        state (bool): The desired power state. True to turn on, False to turn off.
    Returns:
        None
    """
    req = json.dumps({"on":state})
    requests.post(API, req)


def getPowerstate():
    """
    Retrieves the power state of a WLED device.
    Sends a GET request to the WLED device's JSON API endpoint to fetch the current state.
    Parses the JSON response to determine if the device is on or off.
    Returns:
        bool: True if the WLED device is on, False otherwise.
    """
    state = requests.get(f"http://{WLED_HOST}/json/state")
    return json.loads(state.text)["on"]
