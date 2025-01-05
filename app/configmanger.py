from dotenv import load_dotenv
import os
import json


def get_env_variables(env_path):
    with open(env_path) as f:
        env_keys = f.read().splitlines()
    env_dict = {item.split('=')[0]: item.split('=')[1].strip('"') for item in env_keys}
    print(env_dict)
    return env_dict


def load_env():
    ENV_PATH = os.path.join(os.path.dirname(__file__), 'data/.env')
    load_dotenv(dotenv_path=ENV_PATH)
    env_dict = get_env_variables(ENV_PATH)
    json_path = os.path.join(os.path.dirname(__file__), 'static/env.json')
    with open(json_path, 'w') as json_file:
        json.dump(env_dict, json_file, indent=4)


if __name__ == '__main__':
    load_env()
