"""
ThalamOS Application

This module sets up a Flask web application for managing storage items, controlling WLED devices,
interacting with a WiFi scale, and querying an LLM service. It provides various routes for rendering templates,
handling item creation, deletion, and search, as well as retrieving environment configurations,
scale weight, and logging messages.
"""

from typing import Annotated
import json
import os

from flask import (  # pylint: disable=import-error
    Flask,
    request,
    render_template,
    jsonify,
    Response,
)
from flask_cors import CORS  # pylint: disable=import-error
from dotenv import load_dotenv  # pylint: disable=import-error

from logger_config import logger
import Storage_connector
import config_manager
import weigh_fi_manager as wifiscale
import wled_requests
import ollama_manager as ollama

ENV_PATH = os.path.join(os.path.dirname(__file__), "data/.env")
load_dotenv(dotenv_path=ENV_PATH)
IS_SCALE_ENABLED = os.getenv("IS_SCALE_ENABLED").lower() == "true"
app = Flask(__name__)
CORS(app)


@app.route("/")
def index() -> Annotated[str, "search page as a rendered template"]:
    """
    Renders the search page.
    Returns:
        Response: The rendered HTML template for the search page.
    """
    return render_template("search.html")


@app.route("/toggleLight")
def toggle_light() -> Annotated[str, "search page as a rendered template"]:
    """
    Toggles the power state of the WLED device and renders the search template.
    This function changes the power state of the WLED device to the opposite of its current state
    by calling the `changePowerState` method of the `wled_requests` object.
    After toggling the power state,
    it returns the rendered "search.html" template.
    Returns:
        str: The rendered "search.html" template.
    """
    try:
        current_state = wled_requests.get_power_state()
        if current_state is not None:
            wled_requests.change_power_state(not current_state)
            logger.info(f"Toggled WLED power state to: {not current_state}")
        else:
            logger.warning("Unable to toggle WLED power state: Current state is unknown.")
    except Exception as e:
        logger.error(f"Error toggling WLED power state: {e}")
    return render_template("search.html")


@app.route("/createItem")
def create_item() -> Annotated[str, "item creation page as a rendered template"]:
    """
    Renders the template for creating a new item.
    Returns:
        Response: The rendered HTML template for creating a new item.
    """
    return render_template("createItem.html")


@app.route("/sendCreation", methods=["POST"])
def send_creation() -> Annotated[tuple, {"status": str, "status_code": int}]:
    """
    Handle the creation of a new item by processing the incoming JSON request data.
    The function expects a JSON payload with the following structure:
    {
        "info": <json>,
        "type": <str>,
        "name": <str>,
        "position": <str>
    }
    It extracts the necessary information from the JSON payload and attempts to create a new item
    using the Storage_connector.CreateItem method.
    If an exception occurs during the creation process,
    it prints the exception.
    Returns:
        tuple: A dictionary with a status message and an HTTP status code.
    """

    data = request.get_json()
    logger.info(f"Received creation request with data: {data}")
    info = json.dumps(data["info"])
    obj_type = data["type"]
    name = data["name"]
    pos = data["position"]
    try:
        Storage_connector.create_item(
            pos=pos, obj_type=obj_type, name=name, json_data=info
        )
    except Exception as e:
        logger.error(
            f"Failed to create item with name: {name}, type: {obj_type}, position: {pos}. Error: {e}"
        )
        return {"status": "error"}, 500
    return {"status": "created"}, 201


@app.route("/item/<item_id>")
def item(item_id) -> Annotated[str, "item page as a rendered template"]:
    """
    Handles the request to display an item.
    This function performs the following steps:
    1. Changes the power state of the WLED device to on.
    2. Fetches the item details from the storage using the provided item identifier.
    3. Sets the color position on the WLED device based on the fetched item details.
    4. If the fetched item contains additional information,
       it parses the data and renders the 'item.jinja2' template
       with the item details and information.
    6. If the fetched item does not contain additional information,
       it renders the 'item.jinja2' template with only the item details.
    Args:
        item_id (int): The id of the item to display.
    Returns:
        The rendered HTML template for the item.
    """
    wled_requests.change_power_state(True)
    item_sql = Storage_connector.fetch_item(item_id)
    wled_requests.color_pos(item_sql[1])
    logger.info(f"Fetched item details for item_id {item_id}: {item_sql}")
    if item_sql[4]:
        json_info = json.loads(item_sql[4])
        return render_template("item.jinja2", item=item_sql, json=json_info, id=item_id)

    return render_template("item.jinja2", item=item_sql, id=item_id)


@app.route("/item/<item_id>/update", methods=["POST"])
def update_item(item_id) -> Annotated[tuple, {"status": str, "status_code": int}]:
    """
    Updates an item using the Storage_connector and returns a status message.
    Args:
        item_id: The id of the item to be updated.
    Returns:
        A dictionary with a status message and an HTTP status code.
    """
    data = request.get_json()
    logger.info(f"Received update request for item_id {item_id} with data: {data}")
    info = json.dumps(data.get("info", {}))
    obj_type = data.get("type")
    name = data.get("name")
    pos = data.get("position")
    try:
        Storage_connector.update_item(
            item_id=item_id, pos=pos, obj_type=obj_type, name=name, json_data=info
        )
    except Exception as e:
        logger.error(f"Failed to update item with id: {item_id}. Error: {e}")
        return {"status": "error"}, 500
    return {"status": "updated"}, 200


@app.route("/item/<item>/delete")
def delete_item(item_id) -> Annotated[str, "search page as a rendered template"]:
    """
    Deletes an item using the Storage_connector and renders the search.html template.
    Args:
        item_id: The id of the item to be deleted.
    Returns:
        A rendered template for the search page.
    """

    Storage_connector.delete_item(item_id)
    return render_template("search.html")


@app.route("/search/<term>", methods=["GET"])
def search(term) -> Response:
    """
    Search for a term in the storage and return the results in JSON format.
    Args:
        term (str): The term to search for in the storage.
    Returns:
        Response: A Flask Response object containing the search results in JSON format.
    """
    data = Storage_connector.search(term)
    return jsonify(data)


@app.errorhandler(Exception)
def handle_exception(e) -> Exception:
    """
    Handles exceptions by passing through HTTP errors.
    Parameters:
    e (Exception): The exception to handle.
    Returns:
    Exception: The same exception that was passed in.
    """

    # pass through HTTP errors
    return e


@app.route("/config/env")
def get_env() -> Response:
    """
    Retrieve the environment configuration.
    This function uses the config_manager to get the current environment
    configuration and returns it as a JSON response.
    Returns:
        Response: A Flask JSON response containing the environment configuration.
    """
    return jsonify(config_manager.get_env())


@app.route("/config/ollama/models")
def get_ollama_models() -> tuple[Response, int] | Response:
    """
    Fetches the list of available Ollama models.
    Returns:
        Annotated[str, "json response"]: A JSON response containing the list of Ollama models.
    """
    values = ollama.get_ollama_models()
    if not values:
        return jsonify({"status": "Ollama service is not enabled"}), 412
    return jsonify(values)


@app.route("/wifiscale/weight")
def get_weight() -> tuple[Response, int] | Response:
    """
    Retrieve the weight of the scale.
    This function checks if the scale service is enabled by reading the IS_SCALE_ENABLED environment variable.
    If the scale service is not enabled, it returns a JSON response with a status message and HTTP status code 412.
    If the scale service is enabled, it uses the wifiscale module to get the weight of the scale and returns it as a JSON response.
    Returns:
        Response: A Flask JSON response containing the weight of the scale or a status message.
    """
    if IS_SCALE_ENABLED == "False":
        return jsonify({"status": "scale service is not enabled"}), 412

    weight = wifiscale.get_weight()
    return jsonify({"weight": weight})


@app.route("/llm/ask", methods=["POST"])
def ask_llm_question() -> Response:
    """
    Ask a question to the Language Learning Model (LLM) service.
    This function sends a GET request to the LLM service at the specified endpoint
    and returns the response as a JSON object.
    Returns:
        Response: A Flask JSON response containing the response from the LLM service.
    """
    data = request.get_json()
    question = data.get("question")
    logger.info(f"Received question via llm endpoint: {question}")
    response = ollama.ask_question(question)
    return jsonify(response)


@app.route("/log", methods=["POST"])
def log_message() -> Annotated[tuple, {"status": str, "status_code": int}]:
    """
    Logs a message with a specified log level.

    The log level and message content are extracted from the JSON payload of the request.
    If the log level is not provided, it defaults to 'INFO'.
    If the message content is not provided, it defaults to an empty string.

    Returns:
        tuple: A dictionary with a status message and an HTTP status code 201.

    Request JSON structure:
        {
            "level": "DEBUG" | "INFO" | "WARNING" | "ERROR" | "CRITICAL",
            "message": "Your log message here"
        }
    """

    data: Annotated[str, "content of request"] = request.json
    level: Annotated[str, "log level, default value is INFO"] = data.get(
        "level", "INFO"
    )
    message: Annotated[str, "content of log, default value is empty"] = data.get(
        "message", ""
    )

    match level:
        case "DEBUG":
            logger.debug(message)
        case "INFO":
            logger.info(message)
        case "WARNING":
            logger.warning(message)
        case "ERROR":
            logger.error(message)
        case "CRITICAL":
            logger.critical(message)

    return {"status": "created"}, 201


with app.app_context():
    Storage_connector.setup()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
