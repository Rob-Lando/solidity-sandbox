from web3 import Web3
from modules.env_encryptor import (
    get_env_vars,
    key_gen,
    decrypt_env_secret
)

if __name__ == "__main__":
    
    env_vars = get_env_vars(path_to_env_file = "../.env",
                            env_var_names = ["INFURA_API_KEY","SEPOLIA_WALLET"])

    _key = key_gen(verify_json = "verify.json")

    infura_url = f"https://mainnet.infura.io/v3/{decrypt_env_secret(_bin_key = _key, secret_name = 'INFURA_API_KEY')}"

    web3 = Web3(Web3.HTTPProvider(infura_url))

    print(web3.isConnected())

