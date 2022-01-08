# Third party imports
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


def human_date(date):
    """
    * Converts the date to a prettier, more readable date.
    * @arg(obj) date -- the date object from choose_date().
    * @return(str) human_date -- pretty date string, e.g. "Wednesday, 05 May 2021"
    """
    human_date = date.strftime('%A, %m %B %Y')
    return human_date


def choose_date():
    """
    * Asks the user which date to input stats for.
    * Converts input to a date object and runs human_date().
    * @return(obj) date_obj -- the date object.
    * @return(str) date_readable -- pretty date string returned from human_date(). 
    """
    print('\nWhich date would you like to input stats for?')
    date_str = input('Date (format: YYYY-MM-DD): ')
    date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
    date_readable = human_date(date_obj)
    return date_obj, date_readable


def capture_stats(date):
    """
    * Capture stats from the user.
    * @arg(obj) date -- the date object passed from update_stats().
    * @return(dict) statDocument -- MongoDB compatible data structure for the captured stats.
    """
    # Generate a title for ticket section.
    t_title = '** Ticket Stats **'
    print('-' * len(t_title))
    print(t_title)
    print('-' * len(t_title))
    # Capture ticket stats as integers.
    t_advanced = int(input('Number of tickets advanced: '))
    t_pub_comments = int(input('Number of ticket public comments: '))
    t_solved = int(input('Number of tickets solved: '))
    t_q_start = int(input('Number of tickets in queue at shift start: '))
    t_q_end = int(input('Number of tickets in queue at shift end: '))
    # Generate a title for chat section.
    c_title = '** Chat Stats **'
    print('-' * len(c_title))
    print(c_title)
    print('-' * len(c_title))
    # Capture chat stats as integers.
    c_total = int(input('Number of chats handled: '))
    c_wait = int(input('Average chat wait time (in seconds): '))
    c_csat = int(input('Chat CSAT score: '))
    print('=' * 80)

    # Create a dictionary ready for MongoDB.
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
    """
    * Checks the database to see if the date already exists, and proceeds accordingly.
    * @arg(obj) date -- the date object passed from stats_main().
    """
    exist = db.stats.count_documents({"date": date}, limit=1)
    # Capture from the user.
    new_stats = capture_stats(date)
    # If the date exists in the database, updates the existing document.
    if exist:
        db.stats.update_one({"date": date}, {"$set": new_stats})
        print('The stats have been successfully updated!')
    # If the date does not exist in the database, inserts a new document.
    elif not exist:
        db.stats.insert_one(new_stats)
        print('The new stats have been successfully added to the database!')


def proceed(user_input):
    """
    * Handles the user input from a yes/no question.
    * @return(bool) -- True for y, False for n.
    """
    if user_input == 'y':
        return True
    elif user_input == 'n':
        return False
    elif user_input != 'y' and proceed != 'n':
        print('Incorrect input. Please type "y" or "n".')


def continue_input():
    """
    * Asks the user if they'd like input more stats.
    * @return(bool) proceed_yes_no -- True for yes, False for no.
    """
    user_input = input('Would you like to input more stats (y/n)? ')
    proceed_yes_no = proceed(user_input)
    return proceed_yes_no


def stats_main():
    """
    * Main function for inputting/updating stats in the database.
    """
    while True:
        # Run choose_date() to capture date input,
        # and return date object and string.
        date_tpl = choose_date()
        date, date_str = date_tpl

        # If the date exists in the database already, offer to overwrite it.
        # If overwriting or adding new stats, run update_stats().
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

        # Ask the user if they'd like to input more stats.
        # If no, break out of the while loop.
        if not continue_input():
            return


def generate_raw_stats(date):
    title = f'Stats for {date}'
    print('-' * len(title))
    print(title)
    print('-' * len(title))
    print('Tickets advanced: ')
    print('Tickets solved: ')
    print('\n')
    print('Incoming queue: ')
    print('Handoff queue: ')
    print('\n')
    print('Total chats: ')
    print('Wait time: ')
    print('Chat CSAT: ')
