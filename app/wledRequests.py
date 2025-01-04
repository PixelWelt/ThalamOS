import requests
import json
import os
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), 'data/.env')
load_dotenv(dotenv_path=ENV_PATH)

WLED_HOST = os.getenv("WLED_HOST")
print(f'WLED host is: {WLED_HOST}')

API = f"http://{WLED_HOST}/json"

def turnOffLights():
    req = json.dumps({"seg":{"i":[0,50,"000000"]}})
    requests.post(API, req)

def colorPos(pos):
    req = json.dumps({"seg":{"i":[pos, "FF0000"]}})
    requests.post(API, req)

def loadDefaultState():
    req = json.dumps({"ps":1})
    requests.post(API, req)

def changePowerState(state):
    req = json.dumps({"on":state})
    requests.post(API, req)

def getPowerstate():
    state = requests.get(f"http://{WLED_HOST}/json/state")
    return json.loads(state.text)["on"]

