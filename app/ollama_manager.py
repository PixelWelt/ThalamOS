"""
This module manages interactions with the Ollama model and the SQLite database.

It includes functions to set up the Ollama pipeline, check if the Ollama feature is enabled,
fetch Ollama models, convert the storage table to a CSV file, and ask questions to the Ollama model.

Classes:
    SQLQuery: A class to execute SQL queries on the SQLite database.

Functions:
    setup_ollama: Sets up the Ollama pipeline.
    pre_check_ollama_enabled: Checks if the Ollama feature is enabled.
    check_ollama_enabled: A decorator to check if Ollama is enabled before executing a function.
    get_ollama_models: Fetches a list of Ollama models from a specified API endpoint.
    storage_table_to_csv: Converts the 'storage' table from the SQLite database to a CSV file.
    ask_question: Asks a question to the Ollama model using a haystack pipeline.
"""
from functools import wraps
import os
from typing import Annotated, List
import requests
from dotenv import load_dotenv
from haystack import Pipeline, component
from haystack.components.builders import PromptBuilder
from haystack.components.routers import ConditionalRouter
from haystack_integrations.components.generators.ollama import OllamaGenerator
import pandas as pd
from sqlalchemy import create_engine

from logger_config import logger

ENV_PATH: Annotated[str, "path to environment variables"] = os.path.join(
    os.path.dirname(__file__), "data/.env"
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

DATABASE_PATH: Annotated[str, "path to database"] = os.path.join(
    os.path.dirname(__file__), "data/storage.db"
)

prompt_instance = PromptBuilder(
    template="""The table **`storage`** contains information about items stored inside a shelf. It has the following columns: **{{columns}}**.

### Rules for Generating an SQL Query:
1. **Only generate a query if the question is directly answerable using only the `storage` table**.
2. **First, check if the question is about stored items**. If the question is about anything else (e.g., news, weather, prices, etc.), return `"no_answer"` and **do not generate a query**.
3. **The `info` column contains JSON data**. To access specific fields within the JSON, use the appropriate SQL functions for JSON extraction:
   - For **SQLLite**, use `JSON_EXTRACT(info, '$.field_name')` to extract a field.
4. **If the question asks for ordering based on a field inside the `info` JSON** (like `length`), **extract the field from the JSON** and **order by it** (use `CAST(info ->> 'length' AS INTEGER)` for PostgreSQL/SQLite or `CAST(JSON_EXTRACT(info, '$.length') AS UNSIGNED)` for MySQL).
5. **Do not use columns like `id` or `position` for ordering unless explicitly mentioned**. If the question is about sorting based on a JSON value (like `length`), **use the JSON extraction in the `ORDER BY` clause**.
6. **If the question asks for the "longest screw" or something similar**, order by `length` from the JSON data, **not by `id`** or other irrelevant columns.
7. **If the question cannot be answered with the given columns**, return exactly `"no_answer"` (without explanation).
8. **Do not attempt to match unrelated concepts to column names**.
9. **Do not modify the database (no DELETE, UPDATE, or INSERT operations).**
10. **Ensure the query returns the entire row of the matched item**.
11. **Ensure the SQL syntax is correct and valid for SQLite**.
12. **The possible values for the `type` column are: `screw`, `nail`, `display`, `cable`, `misc`, `motor-driver`**. These types are case-sensitive.
13. Always take other columns then info into account when answering the question. For example name or type.


**Output (only one of the following):**
- A valid **SQL query**, that returns the row, that matches the user Request, if and only if the question is **directly answerable**. **Do not output anything except of the sql query**.
- `"no_answer"` (exactly this string) if the question is irrelevant or unanswerable.


**Question:** {{question}}
"""
)

fallback_prompt_instance = PromptBuilder(
    template="""User entered a query that cannot be answerwed with the given table.
                                            The query was: {{question}} and the table had columns: {{columns}}.
                                            Let the user know why the question cannot be answered using the table, but try it to answer with your general knowledge."""
)


@component
class SQLQuery:
    """
    A component to execute SQL queries on the SQLite database.

    Attributes:
        connection (sqlite3.Connection): The connection to the SQLite database.

    Methods:
        run(queries: List[str]) -> dict: Executes the provided SQL queries and returns the results.
    """

    def __init__(self, sql_database: str):
        self.engine = create_engine(f"sqlite:///{os.path.abspath(sql_database)}")

    @component.output_types(results=List[str], queries=List[str])
    def run(self, queries: List[str]):
        """
        Executes the provided SQL queries on the SQLite database and returns the results.
        Args:
            queries (List[str]): A list of SQL query strings to be executed.
        Returns:
            dict: A dictionary containing the results of the executed queries and the original queries.
        """
        results = []
        for query in queries:
            try:
                # pandas kann direkt mit der SQLAlchemy-Engine arbeiten
                df = pd.read_sql(query, self.engine)
                result = df.to_json(orient="records")
                results.append(result)
            except Exception as e:
                logger.error(f"Error executing SQL query: {e}")
                return {"results": ["error"], "queries": queries}

        return {"results": results, "queries": queries}

    def __str__(self):
        return "<SQLQuery Object>"


def setup_ollama():
    """
    Sets up the Ollama pipeline with the necessary components and connections.

    This function initializes the SQLQuery component, defines routing conditions,
    and sets up the ConditionalRouter, OllamaGenerator, and fallback components.
    It then creates a Pipeline, adds the components to it, and connects them
    according to the defined routes.

    Returns:
        Pipeline: The configured Ollama pipeline.
    """
    sql_query = SQLQuery(DATABASE_PATH)

    routes = [
        {
            "condition": "{{'no_answer' not in replies[0]}}",
            "output": "{{replies}}",
            "output_name": "sql",
            "output_type": List[str],
        },
        {
            "condition": "{{'no_answer'|lower in replies[0]|lower}}",
            "output": "{{question}}",
            "output_name": "go_to_fallback",
            "output_type": str,
        },
    ]
    router = ConditionalRouter(routes)
    llm = OllamaGenerator(model=default_model, url=ollama_host)
    fallback_llm = OllamaGenerator(model=default_model, url=ollama_host)

    conditional_sql_pipeline = Pipeline()
    conditional_sql_pipeline.add_component("prompt", prompt_instance)
    conditional_sql_pipeline.add_component("llm", llm)
    conditional_sql_pipeline.add_component("router", router)
    conditional_sql_pipeline.add_component("fallback_prompt", fallback_prompt_instance)
    conditional_sql_pipeline.add_component("fallback_llm", fallback_llm)
    conditional_sql_pipeline.add_component("sql_querier", sql_query)

    conditional_sql_pipeline.connect("prompt", "llm")
    conditional_sql_pipeline.connect("llm.replies", "router.replies")
    conditional_sql_pipeline.connect("router.sql", "sql_querier.queries")
    conditional_sql_pipeline.connect(
        "router.go_to_fallback", "fallback_prompt.question"
    )
    conditional_sql_pipeline.connect("fallback_prompt", "fallback_llm")

    return conditional_sql_pipeline


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
    the `pre_check_ollama_enabled` function. If Ollama is enabled, the wrapped
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


def storage_table_to_csv(path: str) -> pd.DataFrame:
    """
    Converts the 'storage' table from the SQLite database to a CSV file.

    Args:
        path (str): The file path to the SQLite database.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the 'storage' table.
    """
    abs_path = os.path.abspath(path)
    engine = create_engine(f"sqlite:///{abs_path}")
    with engine.connect() as conn:
        table = pd.read_sql_query("SELECT * FROM storage", conn)
    return table


@check_ollama_enabled
def ask_question(msg):
    """
    Asks a question to the Ollama model using a haystack pipeline.

    Args:
        msg (str): The question to ask the Ollama model.

    Returns:
        tuple: A tuple containing the type of response ("Item" or "Fallback") and the response itself.
    """
    table = storage_table_to_csv(DATABASE_PATH)
    columns = table.columns.tolist()
    result = global_Pipeline.run(
        {
            "prompt": {"question": msg, "columns": columns},
            "router": {"question": msg},
            "fallback_prompt": {"columns": columns},
        }
    )

    if "sql_querier" in result:
        result = result["sql_querier"]["results"][0]
        logger.info(
            f"llm answered with the following SQL query: {result} with type {type(result)}"
        )
        return "Item", result
    if "fallback_llm" in result:
        result = result["fallback_llm"]["replies"][0]
        logger.info(
            f"llm answered with the following fallback: {result} with type {type(result)}"
        )
        return "Fallback", result


global_Pipeline = setup_ollama()
