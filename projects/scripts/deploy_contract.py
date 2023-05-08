import shutil
import os
from web3 import Web3
from modules import env_encryptor


def get_env_vars(path_to_env_file: str, env_var_names: list) -> dict:

    env_encryptor.load_env(path_to_env_file)

    env_vars = {var:os.environ[var] for var in env_var_names}

    return env_vars


if __name__ == "__main__":
    
    get_env_vars(path_to_env_file = "../.env", env_var_names = ["INFURA_API_KEY"])

    # clear module cache so latest version is always imported
    module_cache_path = "/".join(env_encryptor.__file__.replace("env_encryptor.py","__pycache__").split("\\")[-2:])
    shutil.rmtree(module_cache_path)
