from flask import Flask, request, render_template, jsonify
import wledRequests
import StorageConnector
import configmanager
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """
    Renders the search page.
    Returns:
        Response: The rendered HTML template for the search page.
    """
    return render_template("search.html")


@app.route('/toggleLight')
def toggleLight():
    """
    Toggles the power state of the WLED device and renders the search template.
    This function changes the power state of the WLED device to the opposite of its current state
    by calling the `changePowerState` method of the `wledRequests` object. After toggling the power state,
    it returns the rendered "search.html" template.
    Returns:
        str: The rendered "search.html" template.
    """
    wledRequests.changePowerState(not wledRequests.getPowerstate())
    return render_template("search.html")


@app.route('/createItem')
def CreateItem():
    """
    Renders the template for creating a new item.
    Returns:
        Response: The rendered HTML template for creating a new item.
    """
    return render_template("createItem.html")


@app.route('/sendCreation', methods=['POST'])
def SendCreation():
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
    using the StorageConnector.CreateItem method. If an exception occurs during the creation process,
    it prints the exception.
    Returns:
        tuple: A dictionary with a status message and an HTTP status code.
    """

    data = request.get_json()
    print(data)
    info = json.dumps(data["info"])
    typ = data["type"]
    name = data["name"]
    pos = data["position"]
    try:
        StorageConnector.CreateItem(pos=pos, typ=typ, name=name, jsonData=info)
    except Exception as e:
        print(e)

    return {"status": "ok"}, 200


@app.route('/item/<item>')
def item(item):
    """
    Handles the request to display an item.
    This function performs the following steps:
    1. Changes the power state of the WLED device to on.
    2. Fetches the item details from the storage using the provided item identifier.
    3. Sets the color position on the WLED device based on the fetched item details.
    4. If the fetched item contains additional information, it parses the data and renders the 'item.jinja2' template with the item details and information.
    6. If the fetched item does not contain additional information, it renders the 'item.jinja2' template with only the item details.
    Args:
        item (int): The id of the item to display.
    Returns:
        The rendered HTML template for the item.
    """
    wledRequests.changePowerState(True)
    item_sql = StorageConnector.fetchItem(item)
    wledRequests.colorPos(item_sql[1])
    print(item_sql)
    if item_sql[4]:
        jsonInfo = json.loads(item_sql[4])
        return render_template("item.jinja2", item=item_sql, json=jsonInfo, id=item)
    else:
        return render_template("item.jinja2", item=item_sql, id=item)


@app.route('/item/<item>/delete')
def deleteItem(item):
    """
    Deletes an item using the StorageConnector and renders the search.html template.
    Args:
        item: The id of the item to be deleted.
    Returns:
        A rendered template for the search page.
    """

    StorageConnector.deleteItem(item)
    return render_template("search.html")


@app.route('/search/<term>',methods=['GET'])
def search(term):
    """
    Search for a term in the storage and return the results in JSON format.
    Args:
        term (str): The term to search for in the storage.
    Returns:
        Response: A Flask Response object containing the search results in JSON format.
    """
    data = StorageConnector.search(term)
    return jsonify(data)


@app.errorhandler(Exception)
def handle_exception(e):
    """
    Handles exceptions by passing through HTTP errors.
    Parameters:
    e (Exception): The exception to handle.
    Returns:
    Exception: The same exception that was passed in.
    """

    # pass through HTTP errors
    return e


@app.route('/config/env')
def getEnv():
    """
    Retrieve the environment configuration.
    This function uses the configmanager to get the current environment
    configuration and returns it as a JSON response.
    Returns:
        Response: A Flask JSON response containing the environment configuration.
    """
    return jsonify(configmanager.get_env())


with app.app_context():
    StorageConnector.setup()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
