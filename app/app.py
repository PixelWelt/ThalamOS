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
    return render_template("search.html")


@app.route('/toggleLight')
def toggleLight():
    wledRequests.changePowerState(not wledRequests.getPowerstate())
    return render_template("search.html")


@app.route('/createItem')
def CreateItem():
    return render_template("createItem.html")


@app.route('/sendCreation', methods=['POST'])
def SendCreation():
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
    StorageConnector.deleteItem(item)
    return render_template("search.html")


@app.route('/search/<term>',methods=['GET'])
def search(term):
    data = StorageConnector.search(term)
    return jsonify(data)


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    return e


@app.route('/config/env')
def getEnv():
    return jsonify(configmanager.get_env())


with app.app_context():
    StorageConnector.setup()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
