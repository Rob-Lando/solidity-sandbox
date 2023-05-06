### Module for manually setting encrypted environment variables and decrypting them:

General Process:

- Take masked user input password and generate hash string using Argon2id from (https://argon2-cffi.readthedocs.io/en/stable/index.html).   
This string contains the password hash & salt, and can be stored visibly in a file named 'verify.json' as initial setup.  
#### Manually generating hash & salt as initial setup  

```python
    import pwinput
    import json
    import argon2
    with open("verify.json","w") as __file__:
        ph = argon2.PasswordHasher()
        hash = ph.hash(pwinput.pwinput(mask = "$"))
        json.dump({"hash":hash},__file__)
```  

- The stored string is used for password verification before generating a key for encryption/decryption.  
Encryption key is generated with a verified masked user input password and the stored salt using https://www.pycryptodome.org/src/protocol/kdf#Crypto.Protocol.KDF.scrypt.  

- Use generated key as input to Salsa20 symmetric encryption algorithm for encrypting or decrypting env vars.  
https://pycryptodome.readthedocs.io/en/latest/src/cipher/salsa20.html  
  
  
## *Note:*  
Currently, Nothing is stopping the verify.json file from being overwritten  
with a new hash string generated from a different user input value  
from someone other than the one who created the last version of the verify.json file.  
Consequently, encrypted env secrets can be overwritten at will.  
However, previously encrypted secrets still will not be able to be decrypted without the previous password  
that created the previous version of the verify.json file.
