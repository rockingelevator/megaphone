import os
import asyncio
import sqlalchemy as sa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from aiopg.sa import create_engine
from src.models import users


backend = default_backend()


def hash_password(pwd, salt=None):
    """
    Generate salt and key for newly given password
    or generate key from pass and salt for verify method
    """
    algorithm = hashes.SHA256()
    iterations = 100000
    salt = salt if salt else os.urandom(16)
    k = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    key = k.derive(pwd.encode())
    salt_to_str = b64encode(salt).decode("utf-8")
    key_to_str = b64encode(key).decode("utf-8")
    return "$".join([algorithm.name, str(iterations), salt_to_str, key_to_str])


@asyncio.coroutine
def verify_password(request):
    data = yield from request.post()
    try:
        email = data['email']
        pwd = data['password']
    except KeyError:
        return {'error': 'Enter email and password'}
    else:
        if not email or not pwd:
            return {'error': 'Enter email and password'}
        else:
            with(yield from request.app['db']) as conn:
                query = sa.select([users]).where(users.c.email == email)
                res = yield from conn.execute(query)
                try:
                    row = list(res)[0]
                except IndexError:
                    return {'error': 'Invalid email/password combination'}
                else:
                    salt_str = row["password"].split('$')[2]
                    salt = b64decode(salt_str)
                    hashed_pwd = hash_password(pwd, salt)
                    if row["password"] == hashed_pwd:
                        return {'error': None,
                                'user_id': row["id"] }
                    else:
                        return {'error': 'Invalid email/password combination'}


if __name__ == "__main__":
    pwd = hash_password("demo123")
    print("Hashed password:", pwd)


