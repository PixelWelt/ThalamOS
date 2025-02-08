"""
This module provides functions to interact with a WLED device via its JSON API.
It allows for turning off lights, setting colors at specific positions, loading default states,
changing power states, and retrieving the current power state of the WLED device.

Functions:
    turn_off_lights(): Sends a request to turn off the lights by setting the segment color to black.
    color_pos(pos): Sends a request to set the color of a specific position on a WLED device.
    load_default_state(): Sends a POST request to the WLED API to load the default state.
    change_power_state(state): Change the power state of the device.
    get_power_state(): Retrieves the power state of a WLED device.
"""
from typing import Annotated
import json
import os

import requests
from dotenv import load_dotenv

from logger_config import logger


ENV_PATH: Annotated[str, "path to environment variables"] = os.path.join(
    os.path.dirname(__file__), "data/.env"
)
load_dotenv(dotenv_path=ENV_PATH)

WLED_HOST: Annotated[str, "environment variable for WLED address"] = os.getenv(
    "WLED_HOST"
)
logger.info(f"WLED host is: {WLED_HOST}")

API: Annotated[str, "URL to WLED"] = f"http://{WLED_HOST}/json"


def turn_off_lights() -> None:
    """
    Sends a request to turn off the lights by setting the segment color to black.
    This function creates a JSON payload to set the color of a segment of lights to black (hex code "000000")
    and sends a POST request to the specified API endpoint to turn off the lights.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    req = json.dumps({"seg": {"i": [0, 50, "000000"]}})
    requests.post(API, req, timeout=10)


def color_pos(pos: int) -> None:
    """
    Sends a request to set the  color of a specific position on a WLED device.
    Args:
        pos (int): The position to set the color for.
    Returns:
        None
    """
    req = json.dumps({"seg": {"i": [pos, "FF0000"]}})
    requests.post(API, req, timeout=10)


def load_default_state() -> None:
    """
    Sends a POST request to the WLED API to load the default state.
    This function creates a JSON payload with a preset state identifier and sends it to the WLED API endpoint using a POST request.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    req = json.dumps({"ps": 1})
    requests.post(API, req, timeout=10)


def change_power_state(state) -> None:
    """
    Change the power state of the device.
    Args:
        state (bool): The desired power state. True to turn on, False to turn off.
    Returns:
        None
    """
    req = json.dumps({"on": state})
    requests.post(API, req, timeout=10)


def get_power_state() -> Annotated[bool, "True if power is on, false if power is off"]:
    """
    Retrieves the power state of a WLED device.
    Sends a GET request to the WLED device's JSON API endpoint to fetch the current state.
    Parses the JSON response to determine if the device is on or off.
    Returns:
        bool: True if the WLED device is on, False otherwise.
    """
    state = requests.get(f"http://{WLED_HOST}/json/state", timeout=10)
    return json.loads(state.text)["on"]
