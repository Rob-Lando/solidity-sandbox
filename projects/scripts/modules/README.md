
### Module for manually setting encrypted environment variables and decrypting them:

General Process:

- Take masked user input password and hash using Argon2id from (https://argon2-cffi.readthedocs.io/en/stable/index.html).  
Generate salt w/ https://pycryptodome.readthedocs.io/en/latest/src/random/random.html#Crypto.Random.get_random_bytes  
This hash and salt can be stored visibly in a file named 'verify.json' as initial setup.  
#### Manually generating hash  
    ```python
    import pwinput
    import json
    import argon2
    with open("verify.json","w") as __file__:
        ph = argon2.PasswordHasher()
        hash = ph.hash(pwinput.pwinput(mask = "$"))
        json.dump({"hash":hash},__file__)
    ```  
    
- The stored hash is used for password verification before generating a key for encryption/decryption with the password and stored salt.  
Encryption key is generated with using https://www.pycryptodome.org/src/protocol/kdf#Crypto.Protocol.KDF.scrypt  
    
- Use generated key as input to Salsa20 symmetric encryption algorithm for encrypting or decrypting env vars.  
https://pycryptodome.readthedocs.io/en/latest/src/cipher/salsa20.html