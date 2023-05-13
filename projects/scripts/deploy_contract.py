from web3 import Web3
from solcx import (
    install_solc, 
    compile_source
)
from modules.env_encryptor import (
    get_env_vars,
    key_gen,
    decrypt_env_secret
)

def compile_sol(path,solc_version)

if __name__ == "__main__":
    
    env_vars = get_env_vars(path_to_env_file = "../.env",
                            env_var_names = ["INFURA_API_KEY","SEPOLIA_WALLET"])

    _key = key_gen(verify_json = "verify.json")

    infura_url = f"https://sepolia.infura.io/v3/{decrypt_env_secret(_bin_key = _key, secret_name = 'INFURA_API_KEY')}"

    w3 = Web3(Web3.HTTPProvider(infura_url))

    print(w3.isConnected())

    install_solc(version = "0.8.0")
    with open('../contracts/bet_ledger.sol', 'r') as sol:
        source = sol.read()

    compiled_src = compile_source(source,
                                 output_values=["abi", "bin-runtime"],
                                 solc_version="0.8.0")
    
    compiled_src = compiled_src[list(compiled_src.keys())[0]]

    print(compiled_src['abi'],"\n\n",compiled_src['bin-runtime'])

    #contract = w3.eth.contract(abi = compiled_src["abi"], bytecode = compiled_src["bin-runtime"])

