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


def update_stats(date):
    exist = db.stats.count_documents({"date": date}, limit=1)
    new_stats = capture_stats(date)
    if exist:
        db.stats.update_one({"date": date}, {"$set": new_stats})
        print('The stats have been successfully updated!')
    elif not exist:
        db.stats.insert_one(new_stats)
        print('The new stats have been successfully added to the database!')
    else:
        print('Something went wrong!')


def proceed(user_input):
    if user_input == 'y':
        return True
    elif user_input == 'n':
        return False
    elif user_input != 'y' and proceed != 'n':
        print('Incorrect input. Please type "y" or "n".')


def continue_input():
    user_input = input('Would you like to input more stats (y/n)? ')
    proceed_yes_no = proceed(user_input)
    return proceed_yes_no


def check_date():
    while True:
        date_tpl = choose_date()
        date, date_str = date_tpl

        if db.stats.count_documents({"date": date}, limit=1):
            print('This date already exists in the database.')
            user_input = input('Would you like to overwrite it (y/n)? ')
            proceed_yes_no = proceed(user_input)
            if proceed_yes_no:
                print(
                    f'\nOkay, let\'s overwrite the stats for {date_str}.')
                update_stats(date)
        else:
            print(f'Please enter the stats for {date_str} below.')
            update_stats(date)

        if not continue_input():
            return
