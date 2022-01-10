# Third party imports
import os
from pymongo import MongoClient
import datetime as dt
from tabulate import tabulate

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
    human_date = date.strftime('%A, %d %B %Y')
    return human_date


def choose_date():
    """
    * Asks the user which date to input/view stats for.
    * Converts input to a date object and runs human_date().
    * @return(obj) date_obj -- the date object.
    * @return(str) date_readable -- pretty date string returned from human_date().
    """
    print('\nWhich date would you like to input stats for?')
    date_str = input('Date (format: YYYY-MM-DD): ')
    date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
    date_readable = human_date(date_obj)
    return date_obj, date_readable


def choose_week():
    """
    * Asks the user which week to view stats for.
    * Converts input to a date object and runs human_date().
    * @return(obj) date_obj -- the date object.
    * @return(str) date_readable -- pretty date string returned from human_date().
    """
    print('\nWhich week would you like to view stats for?')
    date_str = input('Date (format: YYYY-MM-DD): ')
    date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
    wk_start = date_obj - dt.timedelta(days=date_obj.weekday())
    wk_end = wk_start + dt.timedelta(days=6)
    date_readable = human_date(wk_start)
    return wk_start, wk_end, date_readable


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


def generate_daily_stats(date, stats_dict):
    """
    * Create a table of stats for the given date.
    * @arg(obj) date -- the date object passed from stats_daily().
    * @arg(dict) stats_dict -- the dict of stats from the database, passed from stats_daily().
    """
    key_list = ['No. of tickets advanced: ', 'No. of ticket public comments: ', 'No. of tickets solved: ',
                'Incoming ticket queue: ', 'Handoff ticket queue: ', 'Total chats: ', 'Chat wait time: ', 'Chat CSAT: ']
    # Convert the stats_dict values to a list.
    stats_list = list(stats_dict.values())
    # Remove the MongoDB ID and date from the list.
    stats_list = stats_list[2:]
    # Merge the key_list and stats_list to a list of lists to be compatible with tabulate.
    table_list = [list(x) for x in zip(key_list, stats_list)]

    # Generate header to include the date.
    title = f'Stats for {date}'
    print('-' * len(title))
    print(title)
    print('-' * len(title))

    # Print the list as a table.
    print(tabulate(table_list, tablefmt="fancy_grid"))


def generate_weekly_stats(date, key_list, stats_list):
    """
    * Create a table of stats for the given week.
    * @arg(obj) date -- the date object passed from stats_weekly().
    * @arg(list) key_list -- the list of keys from the aggregator, passed from stats_weekly().
    * @arg(list) stats_list -- the list of stats from the database, passed from stats_weekly().
    """
    # Convert the stats values to floats to help table alignment and round ratio value.
    stats_list = [float(x) for x in stats_list]
    stats_list = [round(x, 1) for x in stats_list]
    # Merge the key_list and stats_list to a list of lists to be compatible with tabulate.
    table_list = [list(x) for x in zip(key_list, stats_list)]

    # Generate header to include the date.
    title = f'Stats for week commencing {date}'
    print('-' * len(title))
    print(title)
    print('-' * len(title))

    # Print the list as a table.
    print(tabulate(table_list, tablefmt="fancy_grid", numalign="decimal"))


def stats_daily():
    """
    * Asks the user to choose a date, finds the matching document in the database,
    * then displays that date's stats in a table format.
    """
    # Run choose_date() to capture date input,
    # and return date object and string.
    date_tpl = choose_date()
    date, date_str = date_tpl

    # Find the matching document from MongoDOB
    stats_dict = db.stats.find_one({"date": date})

    generate_daily_stats(date_str, stats_dict)


def stats_weekly():
    # Run choose_date() to capture date input,
    # and return date object and string.
    dates_tpl = choose_week()
    wk_start, wk_end, date_str = dates_tpl

    wk_stats = db.stats.aggregate([
        {
            # Fetch the documents between the week starting and ending dates.
            '$match': {
                'date': {
                    '$gte': wk_start,
                    '$lte': wk_end
                }
            }
        }, {
            # Group the data and calculate the column totals.
            '$group': {
                '_id': 'null',
                'Total tickets advanced': {
                    '$sum': '$t_advanced'
                },
                'Total ticket public comments': {
                    '$sum': '$t_pub_comments'
                },
                'Total tickets solved': {
                    '$sum': '$t_solved'
                },
                'Total chats': {
                    '$sum': '$c_total'
                },
                'Average ticket public comments per day': {
                    '$avg': '$t_pub_comments'
                },
                'Average tickets solved per day': {
                    '$avg': '$t_solved'
                },
                'Average chats per day': {
                    '$avg': '$c_total'
                },
                'Average chat wait time': {
                    '$avg': '$c_wait'
                },
                'Average chat CSAT for the week': {
                    '$avg': '$c_csat'
                }
            }
        }, {
            # Forward the totals through the pipeline and include the comments per solve ratio.
            '$project': {
                'Total tickets advanced': 1,
                'Total ticket public comments': 1,
                'Total tickets solved': 1,
                'Total chats': 1,
                'Average ticket public comments per day': 1,
                'Average tickets solved per day': 1,
                'Average chats per day': 1,
                'Average chat wait time': 1,
                'Average chat CSAT for the week': 1,
                'Average public comments per ticket solved': {
                    '$divide': [
                        '$Average ticket public comments per day', '$Average tickets solved per day'
                    ]
                }
            }
        }
    ])

    temp_list = list(wk_stats)

    stats_list = []
    key_list = []
    for i in temp_list:
        for v in i.values():
            if v != "null":
                stats_list.append(v)
        for k in i.keys():
            if k != "_id":
                key_list.append(k)

    generate_weekly_stats(date_str, key_list, stats_list)
