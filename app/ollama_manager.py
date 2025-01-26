from functools import wraps
import os
from typing import Annotated
import time

import requests
from dotenv import load_dotenv  # pylint: disable=import-error
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_core.prompts import PromptTemplate
from langchain.agents.agent_types import AgentType
from langgraph.prebuilt import create_react_agent

from logger_config import logger

ENV_PATH: Annotated[str, "path to environment variables"] = os.path.join(
    os.path.dirname(__file__), "../data/.env"
)
load_dotenv(dotenv_path=ENV_PATH)
is_ollama_enabled: Annotated[bool, "environment variable for ollama enabled"] = (
    os.getenv("IS_OLLAMA_ENABLED", "false").lower() == "true"
)

ollama_host: Annotated[str, "environment variable for ollama host"] = os.getenv(
    "OLLAMA_HOST"
)
default_model: Annotated[str, "environment variable for default model"] = os.getenv(
    "DEFAULT_MODEL"
)
db = SQLDatabase.from_uri(
    "sqlite:////mnt/f/Dev/4_ThalamOS/StorageManager/data/storage.db"
)

TEMPLATE = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

To start you should ALWAYS look at the tables in the database to see what you can query.
Do NOT skip this step.
Then you should query the schema of the most relevant tables.

The 'storage' table contains the following columns:
    - id: INTEGER, primary key, autoincrement
    - position: INTEGER
    - type: sensor | screw | display | nail | display | cable | miscellaneous | Motor Driver
    - name: TEXT
    - info: TEXT
    - modification_time: TIMESTAMP, defaults to the current timestamp
    The trigger 'update_modification_time' ensures that the 'modification_time' column
    is automatically updated to the current timestamp whenever a row in the 'storage'
    table is updated.
"""


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
    url = f"{ollama_host}/api/tags"
    response = requests.get(url, timeout=10)
    data = response.json()
    models = data.get("models", [])
    model_list = []
    for model in models:
        model_list.append(model["model"])
    return model_list


@check_ollama_enabled
def ask_question(msg, context=None):
    llm = ChatOllama(model=default_model, url=ollama_host)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    system_message = TEMPLATE.format(dialect="SQLite", top_k=5)

    agent_executor = create_react_agent(
        llm, toolkit.get_tools(), state_modifier=system_message
    )

    inputs = {"messages": [("user", msg)]}

    response = agent_executor.invoke(input=inputs)
    print(response)


ask_question(
    "what display should I use for my arduino project? based upon the data in my database?"
)
