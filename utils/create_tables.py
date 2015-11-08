import src.models as models
from src.app import app
from sqlalchemy import create_engine
from src.models import users
from src.auth.users_auth import hash_password

engine = create_engine(app['dsn'])


def create_tables():
    """
    Creates all tables from models.py if not exists
    Run python -m utils.create_tables
    """
    models.metadata.create_all(engine)


def drop_tables():
    models.metadata.drop_all(engine)


def create_demo_user():
    pwd = hash_password("demo123")
    query = users.insert().values(username="demo",
                                  email="demo@demo.com",
                                  password=pwd)
    conn = engine.connect()
    res = conn.execute(query)
    print(res.inserted_primary_key)


if __name__ == "__main__":
    print('Creating tables...')
    drop_tables()
    create_tables()
    create_demo_user()