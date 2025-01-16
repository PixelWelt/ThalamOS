"""
This module provides functionality to read and load environment variables from a .env file.

Functions:
    get_env_variables(env_path: str) -> dict:
    get_env() -> dict:
        Loads environment variables from a .env file and returns them as a dictionary.
"""
from typing import Annotated
import os
from dotenv import load_dotenv

from logger_config import logger


def get_env_variables_from_path(env_path: str) -> Annotated[dict, "dictionary of environment variables"]:
    """
    Reads environment variables from a file and returns them as a dictionary.
    Args:
        env_path (str): The path to the environment variables file.
    Returns:
        dict: A dictionary containing the environment variables as key-value pairs.
    """
    with open(env_path, encoding='utf-8') as f:
        env_keys = f.read().splitlines()
    env_dict = {item.split('=')[0]: item.split('=')[1].strip('"') for item in env_keys}
    logger.debug(f"Environment variables loaded: {env_dict}")
    return env_dict


def get_env() -> Annotated[dict, "dictionary of environment variables"]:
    """
    Loads environment variables from a .env file and returns 
    them as a dictionary.
    Returns:
        dict: A dictionary containing the environment variables.
    """
    env_path = os.path.join(os.path.dirname(__file__), 'data/.env')
    load_dotenv(dotenv_path=env_path)
    env_dict = get_env_variables_from_path(env_path)
    return env_dict


if __name__ == '__main__':
    print(get_env())
