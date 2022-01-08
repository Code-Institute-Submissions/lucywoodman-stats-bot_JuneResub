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


def stat_overwrite():
    while True:
        date = choose_date()

        if db.stats.count_documents({"date": date}, limit=1):
            loop = True
            print('This date already exists in the database.')
            while loop:
                proceed = input('Would you like to overwrite it (y/n)? ')
                if proceed == 'y':
                    print('Okay, let\'s overwrite it.')
                elif proceed == 'n':
                    loop = False
                elif proceed != 'y' and proceed != 'n':
                    print('Incorrect input. Please type "y" or "n".')
        else:
            print('The date does not exist.')
