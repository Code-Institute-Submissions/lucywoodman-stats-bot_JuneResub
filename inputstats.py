import os
from pymongo import MongoClient
import datetime as dt

# Local application imports
if os.path.exists('settings.py'):
    from settings import mongodb_string

# Connect to MongoDB and set the database variables
client = MongoClient(mongodb_string)
db = client.supportStats
stats = db.stats


def choose_date():
    print('Which date would you like to input stats for?')
    date_str = input('Date (format: YYYY-MM-DD): ')
    date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d').date()
    print(date_obj)
    return date_obj
