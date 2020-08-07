"""
Copyright (C) 2010
Author: Yann GUIBET
Contact: <yannguibet@gmail.com>

Python OpenSSL wrapper.
For modern cryptography with ECC, AES, HMAC, Blowfish, ...

This is an abandoned package maintained inside of the PyBitmessage.
"""
try:
    from pyelliptic.cipher import Cipher
    from pyelliptic.ecc import ECC
    from pyelliptic.eccblind import ECCBlind
    from pyelliptic.eccblindchain import ECCBlindChain
    from pyelliptic.hash import hmac_sha256, hmac_sha512, pbkdf2
    from pyelliptic.openssl import OpenSSL
except:
    from pybitmessage.pyelliptic.cipher import Cipher
    from pybitmessage.pyelliptic.ecc import ECC
    from pybitmessage.pyelliptic.eccblind import ECCBlind
    from pybitmessage.pyelliptic.eccblindchain import ECCBlindChain
    from pybitmessage.pyelliptic.hash import hmac_sha256, hmac_sha512, pbkdf2
    from pybitmessage.pyelliptic.openssl import OpenSSL


__version__ = '1.3'

__all__ = [
    'OpenSSL',
    'ECC',
    'ECCBlind',
    'ECCBlindChain',
    'Cipher',
    'hmac_sha256',
    'hmac_sha512',
    'pbkdf2'
]
