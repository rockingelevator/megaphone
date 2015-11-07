import models as models
from app import app
from sqlalchemy import create_engine


def create_tables():
    """
    Creates all tables from models.py if not exists
    Run python -m utils.create_tables
    """
    engine = create_engine(app['dsn'])
    models.metadata.create_all(engine)

if __name__ == "__main__":
    print('Creating tables...')
    create_tables()