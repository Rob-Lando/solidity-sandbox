

Module for manually setting encrypted environment variables and decrypting them:
        Encryption process:
            - takes masked user input password and hash using Argon2id from (https://argon2-cffi.readthedocs.io/en/stable/index.html), this hash and salt can be stored visibly in a json file as initial setup
            - this stored hash can be checked against to verify correct password input
            - if user input is the correct password, generate a 32 byte encryption key with it using https://www.pycryptodome.org/src/protocol/kdf#Crypto.Protocol.KDF.scrypt
            - use generated key as input to Salsa20 symmetric encryption algorithm for encrypting or decrypting env vars.