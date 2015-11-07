import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
backend = default_backend()


def make_key(pwd):
    """
    Generate salt and key for given password
    """
    salt = os.urandom(16)
    k = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    return {
        "salt": salt,
        "key": k.derive(str.encode(pwd))
    }


def verify_password(user_id, pwd):
    """
    Verify given password
    """
    # TODO
    pass


if __name__ == "__main__":
    key = make_key("awesome_password")
    print("Key:")
    print(key["key"])
    print("Salt:")
    print(key["salt"])
