import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def alg(password):
    salt = b'876543256777777'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_256(),
        length=32,
        salt=salt,
        iterations=300000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    return f


data = input('Enter the data: ')
pwd = getpass.getpass('Enter password:').encode('utf-8')

f = alg(pwd)
encrypted = f.encrypt(str.encode(data))
encrypted = encrypted.decode('utf-8')

print(encrypted)
input()
