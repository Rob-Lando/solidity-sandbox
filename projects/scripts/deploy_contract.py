import shutil
from web3 import Web3
from modules import env_encryptor



def main(path_to_env_file: str, env_var_names: list):

    env_encryptor.load_env("../.env")

    _env_vars = {var:env_encryptor.decrypt_env_secret(secret_name = var) for var in env_var_names}


if __name__ == "__main__":
    
    main(path_to_env_file = "../.env", env_var_names = ["INFURA_API_KEY"])

    # clear module cache so latest version is always imported
    module_cache_path = "/".join(env_encryptor.__file__.replace("env_encryptor.py","__pycache__").split("\\")[-2:])
    shutil.rmtree(module_cache_path)
