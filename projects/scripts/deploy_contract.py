from web3 import Web3
from Crypto.Hash import keccak
from Crypto.Cipher import Salsa20
import pwinput
import os

def get_masked_user_input(prompt):

    user_input = pwinput.pwinput(f"\n\n{prompt}:", mask = "$")

    return user_input

def hash_user_input():

    user_input = get_masked_user_input("Enter value to hash: ")

    keccak256 = keccak.new(digest_bits = 256)

    keccak256.update(bytes(user_input,'utf-8'))

    del user_input

    return keccak256.digest(),keccak256.hexdigest()

def encrypt_secret(key: bytes, secret_to_encrypt: str) -> bytes:

    secret_to_encrypt = bytes(secret_to_encrypt,'utf-8') # this is the value we want to encrypt

    cipher = Salsa20.new(key = key)

    msg = cipher.nonce + cipher.encrypt(secret_to_encrypt)

    #print(f"\n\nencrypted_secret is:-> {msg} | {type(msg)}")

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



def decrypt_env_secret(key: bytes, secret_name: str):


    #print(f"\n\nsecret after pulling from env | {os.environ.get(secret_name)}\n{type(os.environ.get(secret_name))}")

    encrypted_secret = bytes.fromhex(os.environ.get(secret_name))

    #print(f"\n\nconverting back to bytes: {encrypted_secret}")

    nonce = encrypted_secret[:8]
    ciphertext = encrypted_secret[8:]

    cipher = Salsa20.new(key = key, nonce = nonce)

    plaintext = cipher.decrypt(ciphertext)

    #print(f"\n\ndecrypted secret: {plaintext}")

    return plaintext


if __name__ == "__main__":

    env_path = '../.env'

    bin_key,hex_key = hash_user_input() # hash user input encryption key to 256 bit size

    msg = encrypt_secret(key = bin_key, secret_to_encrypt = "flip the patty!") # encrypt secret using hashed encryption key

    write_encrypted_secret_to_env(encrypted_secrets = {'GRILLING_TASK':msg.hex()},
                                  path_to_env_file = env_path) # write encrypted secret to local .env file

    load_env(path_to_env_file = env_path) # load variables in .env file to environment

    decrypt_env_secret(key = bin_key, secret_name = 'GRILLING_TASK') # decrypt secret from env using hashed encryption key