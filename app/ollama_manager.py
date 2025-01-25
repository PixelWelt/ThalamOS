from functools import wraps
import os
from typing import Annotated

import requests
from dotenv import load_dotenv

from logger_config import logger

ENV_PATH: Annotated[str, "path to environment variables"] = os.path.join(
    os.path.dirname(__file__), "../data/.env"
)
load_dotenv(dotenv_path=ENV_PATH)
is_ollama_enabled: Annotated[bool, "environment variable for ollama enabled"] = (
    os.getenv("IS_OLLAMA_ENABLED", "false").lower() == "true"
)


def pre_check_ollama_enabled():
    """
    Checks if the Ollama feature is enabled.
    Returns:
        bool: True if the Ollama feature is enabled, False otherwise.
    """
    if is_ollama_enabled:
        return True
    return False


def check_ollama_enabled(func):
    """
    Decorator to check if Ollama is enabled before executing the function.
    This decorator wraps a function and checks if Ollama is enabled by calling
    the `pre_check_ollam_enabled` function. If Ollama is enabled, the wrapped
    function is executed. Otherwise, a log message is generated, and the function
    execution is skipped.
    Args:
        func (callable): The function to be wrapped by the decorator.
    Returns:
        callable: The wrapped function that includes the Ollama enabled check.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if pre_check_ollama_enabled():
            return func(*args, **kwargs)

        logger.info(
            f"Ollama is not enabled. Execution of function {func.__name__} skipped."
        )
        return None

    return wrapper


@check_ollama_enabled
def get_ollama_models():
    """
    Fetches a list of Ollama models from a specified API endpoint.
    This function sends a GET request to the API endpoint at "http://10.45.2.60:11434/api/tags",
    retrieves the JSON response, and extracts the list of models from the response data.
    Returns:
        list: A list of model names (strings) retrieved from the API response.
    """
    url = "http://10.45.2.60:11434/api/tags"
    response = requests.get(url)
    data = response.json()
    models = data.get("models", [])
    model_list = []
    for model in models:
        model_list.append(model["model"])
    return model_list
