from dotenv import load_dotenv
import os


def get_env_variables(env_path: str) -> dict:
    with open(env_path) as f:
        env_keys = f.read().splitlines()
    env_dict = {item.split('=')[0]: item.split('=')[1].strip('"') for item in env_keys}
    print(env_dict)
    return env_dict


def get_env() -> dict:
    """
    Loads environment variables from a .env file and returns 
    them as a dictionary.
    Returns:
        dict: A dictionary containing the environment variables.
    """
    ENV_PATH = os.path.join(os.path.dirname(__file__), 'data/.env')
    load_dotenv(dotenv_path=ENV_PATH)
    env_dict = get_env_variables(ENV_PATH)
    return env_dict


if __name__ == '__main__':
    print(get_env())
