from flask import Flask, request, render_template
import wledRequests
import StorageConnector
import json

app = Flask(__name__)
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
    except  Exception as e:
        print(e)

    return {"status": "ok"}, 200

@app.route('/item/<item>')
def item(item):
    wledRequests.changePowerState(True)
    item_sql = StorageConnector.fetchItem(item)
    wledRequests.colorPos(item_sql[0])
    print(item_sql[3])
    if item_sql[3]:
        jsonInfo = json.loads(item_sql[3])
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
    return data


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    
    return e


if __name__ == '__main__':
    app.run()
