import os
import asyncio
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
backend = default_backend()
from base64 import b64encode, b64decode
from src.app import app
import sqlalchemy as sa
from aiopg.sa import create_engine
from src.models import users

#from manage import loop


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
def verify_password(user_id, pwd):
    """
    Verify given password
    """

    # TODO
    # replace params with request
    # aftre that remove engine initialisation here, there is db_middleware

    engine = yield from create_engine(app["dsn"])
    with (yield from engine) as conn:
        query = sa.select([users]).where(users.c.id == user_id)
        res = yield from conn.execute(query)
        for row in res:
            salt_str = row["password"].split('$')[2]
            salt = b64decode(salt_str)
            hashed_pwd = hash_password(pwd, salt)
            print(row["password"] == hashed_pwd) # Test
            return row["password"] == hashed_pwd


if __name__ == "__main__":
    pwd = hash_password("demo123")
    print("Hashed password:", pwd)
    print("Verifying password:")
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(verify_password(1, 'demo123'))
    loop.run_forever()
    loop.close()


