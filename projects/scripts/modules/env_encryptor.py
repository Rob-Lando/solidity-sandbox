from Crypto.Hash import keccak
from Crypto.Cipher import Salsa20
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import argon2
import pwinput
import json
import os

def get_masked_user_input(prompt):

    user_input = pwinput.pwinput(f"\n\n{prompt}:", mask = "$")

    return user_input

def hash_value(val: str):

    keccak256 = keccak.new(digest_bits = 256)

    keccak256.update(bytes(val,'utf-8'))

    del val

    return keccak256.digest(),keccak256.hexdigest()

def verify_password(verify_json):

    """
    Verify password and rehash if needed.
    """

    ph = argon2.PasswordHasher()
    
    with open(verify_json,"r") as verify:

        stored_hash = json.load(verify) 

        _pwd = pwinput.pwinput(mask = "$")

        ph.verify(stored_hash['hash'],_pwd)

        if ph.check_needs_rehash(stored_hash['hash']):

            with open(verify_json,"w") as verify:
                
                new_hash = {"hash":ph.hash(_pwd)}
                
                json.dump(new_hash, verify)
    
    return _pwd

def salt_gen(verify_json):

    """
    Generate and store salt for key gen/verification.
    """

    _pwd = verify_password(verify_json = verify_json)

    salt = get_random_bytes(16)
    
    # store salt in verify_json
    with open(verify_json, "r") as __file__:

        verify = json.load(__file__)

        verify["key_salt"] = salt.hex()

    with open(verify_json, "w") as __file__:

        json.dump(verify,__file__)

    return None

def key_gen(verify_json):

    """Generate encryption key using stored salt"""

    _pwd = verify_password(verify_json = verify_json)

    with open(verify_json, "r") as __file__:

        verify = json.load(__file__)

        salt = bytes.from_hex(verify["key_salt"])
    
    _key = scrypt(password = _pwd, salt = salt, key_len = 32, N=2**14, r=8, p=1)

    return _key

def encrypt_secret(key: bytes, secret_to_encrypt: str) -> bytes:

    cipher = Salsa20.new(key = key)

    secret_to_encrypt = bytes(secret_to_encrypt,'utf-8') # this is the value we want to encrypt

    msg = cipher.nonce + cipher.encrypt(secret_to_encrypt)

    del secret_to_encrypt

    msg = msg.hex()

    print(f"\n\nencrypted_secret is:-> {msg} | {type(msg)}")

    return msg

def write_encrypted_secret_to_env(encrypted_secrets: dict, path_to_env_file: str):

    with open(path_to_env_file, "w") as f:

        f.write("") # clear existing .env file

        for key,value in encrypted_secrets.items():

            f.write(f"{key}={value}")
            f.write("\n")

    return None


def load_env(path_to_env_file):

    with open(path_to_env_file,'r') as f:

        for line in f:

            key, value = line.strip().split('=')
            os.environ[key] = value

    return None



def setup_env(env_path, verify_json):
        
    _bin_key = key_gen(verify_json = verify_json)

    secret_name = input("\nType the name of the secret you want to encrypt:")

    msg = encrypt_secret(key = _bin_key,
                            secret_to_encrypt = get_masked_user_input(f"Now type its secret value\n{secret_name}")) # encrypt secret using hashed encryption key

    write_encrypted_secret_to_env(encrypted_secrets = {secret_name:msg},
                                    path_to_env_file = env_path) # write encrypted secret to local .env file as hex

    load_env(path_to_env_file = env_path) # load variables in .env file to environment
    
    del _bin_key

    return None


def decrypt_env_secret(secret_name: str, verify_json: str):

    encrypted_secret = bytes.fromhex(os.environ.get(secret_name))

    nonce = encrypted_secret[:8]
    ciphertext = encrypted_secret[8:]

    _bin_key = key_gen(verify_json = verify_json)

    cipher = Salsa20.new(key = _bin_key, nonce = nonce)

    decrypted_secret = str(cipher.decrypt(ciphertext))

    return decrypted_secret
