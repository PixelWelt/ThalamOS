"""
This module provides functionality to read and load environment variables from a .env file.

Functions:
    get_env_variables(env_path: str) -> dict:
    get_env() -> dict:
        Loads environment variables from a .env file and returns them as a dictionary.
"""
from typing import Annotated
import os
from dotenv import load_dotenv  # pylint: disable=import-error
import pytest

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


# Tests

def test_get_env_variables_from_path(tmp_path):
    """
    Test the get_env_variables_from_path function.
    This test creates a temporary .env file with predefined key-value pairs,
    calls the get_env_variables_from_path function with the path to the temporary
    .env file, and asserts that the returned dictionary contains the expected
    key-value pairs.
    Args:
        tmp_path (pathlib.Path): A temporary directory path provided by pytest.
    Raises:
        AssertionError: If the returned dictionary does not match the expected key-value pairs.
    """

    # Create a temporary .env file
    env_file = tmp_path / ".env"
    env_file.write_text('KEY1="value1"\nKEY2="value2"\n')

    # Call the function with the path to the temporary .env file
    env_vars = get_env_variables_from_path(str(env_file))

    # Assert that the returned dictionary contains the expected key-value pairs
    assert env_vars == {
        "KEY1": "value1",
        "KEY2": "value2"
    }


def test_get_env_variables_from_path_empty_file(tmp_path):
    """
    Test case for get_env_variables_from_path function with an empty .env file.
    This test creates an empty temporary .env file and calls the 
    get_env_variables_from_path function with the path to this file. 
    It then asserts that the returned dictionary is empty.
    Args:
        tmp_path (pathlib.Path): A temporary directory path provided by pytest.
    """

    # Create an empty temporary .env file
    env_file = tmp_path / ".env"
    env_file.write_text('')

    # Call the function with the path to the empty .env file
    env_vars = get_env_variables_from_path(str(env_file))

    # Assert that the returned dictionary is empty
    assert env_vars == {}


def test_get_env_variables_from_path_invalid_format(tmp_path):
    """
    Test case for get_env_variables_from_path function to handle invalid format in .env file.
    This test creates a temporary .env file with an invalid format and verifies that the 
    get_env_variables_from_path function raises an IndexError when attempting to parse it.
    Args:
        tmp_path (pathlib.Path): Temporary directory provided by pytest to create the .env file.
    Raises:
        IndexError: Expected exception when the .env file contains an invalid format.
    """
    
    # Create a temporary .env file with invalid format
    env_file = tmp_path / ".env"
    env_file.write_text('KEY1="value1"\nINVALID_LINE\nKEY2="value2"\n')

    # Call the function with the path to the temporary .env file
    with pytest.raises(IndexError):
        get_env_variables_from_path(str(env_file))