from src import models
from src.app import app
from sqlalchemy import create_engine
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
    pwd2 = hash_password("123456")
    records = [
        {
            "username": "demo",
            "email": "demo@demo.com",
            "password": pwd
        },
        {
            "username": "test",
            "email": "test@test.com",
            "password": pwd2
        }
    ]
    conn = engine.connect()
    conn.execute(models.users.insert(), records)


def create_demo_team():
    query = models.teams.insert().values(
        name="Demo Team",
        slug="demo-team",
        owner=1
    )
    conn = engine.connect()
    conn.execute(query)
    add_owner_relation = models.teams_users.insert().values(
        team=1,
        user=1
    )
    conn.execute(add_owner_relation)


if __name__ == "__main__":
    print('Creating tables...')
    drop_tables()
    create_tables()
    create_demo_user()
    create_demo_team()