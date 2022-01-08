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
    print('\nWhich date would you like to input stats for?')
    date_str = input('Date (format: YYYY-MM-DD): ')
    date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
    date_readable = date_obj.strftime('%A, %m %B %Y')
    return date_obj, date_readable


def capture_stats(date):
    t_title = '** Ticket Stats **'
    print('-' * len(t_title))
    print(t_title)
    print('-' * len(t_title))
    t_advanced = int(input('Number of tickets advanced: '))
    t_pub_comments = int(input('Number of ticket public comments: '))
    t_solved = int(input('Number of tickets solved: '))
    t_q_start = int(input('Number of tickets in queue at shift start: '))
    t_q_end = int(input('Number of tickets in queue at shift end: '))
    c_title = '** Chat Stats **'
    print('-' * len(c_title))
    print(c_title)
    print('-' * len(c_title))
    c_total = int(input('Number of chats handled: '))
    c_wait = int(input('Average chat wait time (in seconds): '))
    c_csat = int(input('Chat CSAT score: '))
    print('=' * 80)

    statDocument = {
        "date": date,
        "t_advanced": t_advanced,
        "t_pub_comments": t_pub_comments,
        "t_solved": t_solved,
        "t_q_start": t_q_start,
        "t_q_end": t_q_end,
        "c_total": c_total,
        "c_wait": c_wait,
        "c_csat": c_csat
    }

    return statDocument


def overwrite_stats(date, date_str):
    try:
        db.stats.count_documents({"date": date}, limit=1)
    except:
        print('Can\'t find the date in the database.')
    else:
        new_stats = capture_stats(date)
        db.stats.update_one({"date": date}, {"$set": new_stats})
        print('The stats have been successfully updated!')


def check_date():
    while True:
        date_tpl = choose_date()
        date, date_str = date_tpl

        if db.stats.count_documents({"date": date}, limit=1):
            loop = True
            print('This date already exists in the database.')
            while loop:
                proceed = input('Would you like to overwrite it (y/n)? ')
                if proceed == 'y':
                    print(
                        f'\nOkay, let\'s overwrite the stats for {date_str}.')
                    overwrite_stats(date, date_str)
                    loop = False
                elif proceed == 'n':
                    loop = False
                elif proceed != 'y' and proceed != 'n':
                    print('Incorrect input. Please type "y" or "n".')
        else:
            print('The date does not exist.')
            # input_new_stats()
