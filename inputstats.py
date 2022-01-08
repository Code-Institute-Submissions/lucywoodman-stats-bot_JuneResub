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
    date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
    print(date_obj)
    return date_obj


def stat_input():
    date = choose_date()

    if db.stats.count_documents({"date": date}, limit=1):
        print('The date exists.')
    else:
        print('The date does not exist.')
