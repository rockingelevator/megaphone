import datetime
import src.models as models
from sqlalchemy import create_engine
from random import randint
from src.app import app

NOTIFICATION_TYPE = [
    'Important',
    'Lunch',
    'Information',
    'Party'
]

engine = create_engine(app['dsn'])


def fill_notifications():
    records = []
    for i in range(40):
        rec = {
            'team': 1,
            'author_id': 1,
            'type': NOTIFICATION_TYPE[randint(0,3)],
            'message': "This is " + str(i) + "'s notification",
            'creation_date': datetime.datetime.now()
        }
        records.append(rec)
    conn = engine.connect()
    conn.execute(models.notifications.insert(), records)


if __name__ == "__main__":
    print("Filling dummy data to notifications")
    fill_notifications()
