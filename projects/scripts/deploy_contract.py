import os
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

def set_solc(version):

    compiler_versions = [cmplr.split("v")[-1] for cmplr in os.listdir(f"{os.path.expanduser('~')}/.solcx")]

    print(f"\n\nAvailable compiler versions are:{compiler_versions}\n\n")

    if version not in compiler_versions:
        install_solc(version = version)
    
    return version

if __name__ == "__main__":
    
    env_vars = get_env_vars(path_to_env_file = "../.env",
                            env_var_names = ["INFURA_API_KEY","SEPOLIA_WALLET"])

    _key = key_gen(verify_json = "verify.json")

    infura_url = f"https://sepolia.infura.io/v3/{decrypt_env_secret(_bin_key = _key, secret_name = 'INFURA_API_KEY')}"

    w3 = Web3(Web3.HTTPProvider(infura_url))

    print(f"\n\nConnected: {w3.is_connected()}\n\n")
    print(f"\n\nGAS PRICE IS: {w3.eth.gas_price} Wei\n\n")

    deployer_account = w3.eth.account.from_key(
                            private_key = decrypt_env_secret(_bin_key = _key,secret_name = 'SEPOLIA_WALLET')
                        )

    # compile contract
    with open('../contracts/bet_ledger.sol', 'r') as sol:
        source = sol.read()

    compiled_src = compile_source(
                                    source,
                                    output_values = ["abi", "bin-runtime"],
                                    solc_version = set_solc("0.8.0")
                                )
    
    contract_id = list(compiled_src.keys())[0].split(":")[1]
    compiled_src = compiled_src[list(compiled_src.keys())[0]]

    print(f"""{contract_id}\n\n{compiled_src['abi']}\n\n<{compiled_src['bin-runtime']}>""")

    contract = w3.eth.contract(abi = compiled_src["abi"], bytecode = compiled_src["bin-runtime"])
    gas_estimate = contract.constructor().estimate_gas()

    print(f"\n\nContract gas estimate is: {gas_estimate} Wei\n\n")

    """
    transaction = contract.constructor().build_transaction(
                    {
                        'from':     w3.to_checksum_address(deployer_account.address),
                        'gas':      gas_estimate,
                        'gasPrice': w3.eth.gas_price,
                        'nonce':    w3.eth.get_transaction_count(deployer_account.address),
                    }
                )
    
    signed_transaction = deployer_account.sign_transaction(transaction)
    """


    #print(list(contract.functions))
