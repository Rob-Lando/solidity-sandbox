from pwinput import pwinput
from Crypto.Cipher import Salsa20
from Crypto.Protocol.KDF import scrypt
import platform
import base64
import argon2
import json
import stat
import os


def set_to_read_only(file_path: str) -> None:

    operating_system = platform.system()

    if operating_system == "Windows":

        os.chmod(file_path, mode = stat.S_IWRITE|stat.S_IREAD)

    else:
        # Will modify later to work with other os
        raise ValueError

    return None

def store_argon2_hash_as_json(json_path: str) -> None:

    with open(json_path,"w") as __file__:

        ph = argon2.PasswordHasher()

        hash = ph.hash(pwinput(mask = "$"))

        json.dump({"hash":hash},__file__)

        set_to_read_only(json_path)

    return None

def verify_password(verify_json: str) -> str:

    """
    Verify password and rehash if needed.
    """

    ph = argon2.PasswordHasher()
    
    with open(verify_json,"r") as verify:

        stored_hash = json.load(verify) 

        _pwd = pwinput(mask = "$")

        ph.verify(stored_hash['hash'],_pwd)

        if ph.check_needs_rehash(stored_hash['hash']):

            with open(verify_json,"w") as verify:
                
                new_hash = {"hash":ph.hash(_pwd)}
                
                json.dump(new_hash, verify)
    
    return _pwd


def key_gen(verify_json: str) -> bytes:

    """Generate encryption key using stored salt"""

    _pwd = verify_password(verify_json = verify_json)

    with open(verify_json, "r") as __file__:

        verify = json.load(__file__)
        stored_hash = verify['hash']

    salt_base64 = stored_hash.split('$')[4]
    missing_padding = 4 - len(salt_base64) % 4
    salt_base64_padded = salt_base64 + '=' * missing_padding

    salt = base64.b64decode(salt_base64_padded)
    
    _key = scrypt(password = _pwd, salt = salt, key_len = 32, N=2**14, r=8, p=1)

    del _pwd

    return _key


def encrypt_secret(key: bytes, secret_to_encrypt: str) -> bytes:

    cipher = Salsa20.new(key = key)

    secret_to_encrypt = bytes(secret_to_encrypt,'utf-8')

    msg = cipher.nonce + cipher.encrypt(secret_to_encrypt)

    del secret_to_encrypt

    msg = msg.hex()

    print(f"\n\nencrypted_secret is:-> {msg} | {type(msg)}")

    return msg


def write_encrypted_secrets_to_env(encrypted_secrets: dict, path_to_env_file: str) -> None:

    with open(path_to_env_file, "w") as f:

        f.write("") # clear existing .env file

        for key,value in encrypted_secrets.items():

            f.write(f"{key}={value}")
            f.write("\n")

    return None


def load_env(path_to_env_file: str) -> None:

    with open(path_to_env_file,'r') as f:

        for line in f:

            key, value = line.strip().split('=')
            os.environ[key] = value

    return None


def setup_env(env_path: str, verify_json: str, read_only: bool = True) -> None:
        
    _bin_key = key_gen(verify_json = verify_json)
    
    encrypted_secrets = {}

    while True:
        add_another = None
        secret_name = input("\n\nType the name of the secret you want to encrypt:")
        encrypted_secrets[secret_name] = encrypt_secret(
                                            key = _bin_key,
                                            secret_to_encrypt = pwinput(
                                                                prompt = f"\n\nNow type its secret value {secret_name}",
                                                                mask = "$"
                                                            )
                                    )
        while True:
            try:
                add_another = input("Would you like to add another secret? (y/n)").strip().lower()
                assert add_another in ['y','n']
                break
            except AssertionError:
                print("Please type y for 'yes' or n for 'no'")
                continue

        if add_another == "y":
            continue
        else:
            break

    del _bin_key

    write_encrypted_secrets_to_env(encrypted_secrets = encrypted_secrets,
                                    path_to_env_file = env_path)

    if read_only:
        set_to_read_only(file_path = env_path)

    load_env(path_to_env_file = env_path)

    return None

def get_env_vars(path_to_env_file: str, env_var_names: list) -> dict:

    load_env(path_to_env_file)

    env_vars = {var:os.environ[var] for var in env_var_names}

    return env_vars

def decrypt_env_secret(_bin_key: bytes, secret_name: str) -> str:

    encrypted_secret = bytes.fromhex(os.environ.get(secret_name))

    nonce = encrypted_secret[:8]
    ciphertext = encrypted_secret[8:]

    cipher = Salsa20.new(key = _bin_key, nonce = nonce)

    decrypted_secret = cipher.decrypt(ciphertext).decode('utf-8')

    return decrypted_secret
