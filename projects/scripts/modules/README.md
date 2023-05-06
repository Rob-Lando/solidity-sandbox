
### Module for manually setting encrypted environment variables and decrypting them:

Encryption process:

- takes masked user input password and hashes using Argon2id from (https://argon2-cffi.readthedocs.io/en/stable/index.html),  
this hash and salt can be stored visibly in a json file as initial setup.  
    
- The hash is used for password verification before generating a key for encryption/decryption with the pwd and a stored salt.  
Encryption key is generated with using https://www.pycryptodome.org/src/protocol/kdf#Crypto.Protocol.KDF.scrypt  
    
- use generated key as input to Salsa20 symmetric encryption algorithm for encrypting or decrypting env vars.