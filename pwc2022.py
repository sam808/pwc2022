#!/usr/bin/env python3

import os

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.backends import default_backend

####################################################################################################
#
# key:
#     A byte string containing the key to be used with this encryption
# iv:
#     Initialization vector to be used for the encryption
# mode:
#     GCM - we'll be using this because it does not require padding and has an additional
#     authentication tag and is relatively simple; lots of other modes are available for Python
# cipher:
#     AES256 - generally the most common in the US for general purpose, but Python has support
#     for a number of other ciphers
#
# See https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption for great docs
#
####################################################################################################

super_secret_text = b"The world needs more pizza"

key = os.urandom(32) # but where would we get the key?
iv = os.urandom(16) # and where would we store the IV?

encryptor = Cipher(
    algorithms.AES(key),
    modes.GCM(iv), # could use CBC
    default_backend() # with 3.6.9 this still throws an error if not included; shouldn't need it anyway
).encryptor()

cipher_text = encryptor.update(super_secret_text) + encryptor.finalize()

tag = encryptor.tag

decryptor = Cipher(
    algorithms.AES(key),
    modes.GCM(iv, tag),
    default_backend()
).decryptor()

plain_text = decryptor.update(cipher_text) + decryptor.finalize()

print(super_secret_text)
print(cipher_text)
print(plain_text)