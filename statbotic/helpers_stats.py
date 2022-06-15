import os
import traceback
from bson.json_util import dumps
from statbotic.title import Title
from statbotic.database import data, test_database, aggregate_data, fetch_data_range
from statbotic.helpers import user_continue, create_lists, print_stats
from statbotic.date import Date
from statbotic.stats import Stats


def new_stats(user_date, *action):
    Title('** ZenDesk Stats **').display()
    stats = Stats()
    stats.date = user_date.date
    stats.comments = int(input('Number of ticket responses: '))
    stats.solves = int(input('Number of ticket solves: '))
    Title('** Intercom Stats **').display()
    stats.total = int(input('Total number of chats: '))
    stats.wait = int(input('Average chat wait time (in seconds): '))
    stats.csat = int(input('Chat CSAT score: '))
    if 'overwrite' in action:
        data.stats.update_one({"date": user_date.date}, {
            "$set": stats.__dict__})
        print('\n** The stats have been successfully updated! **\n')
    elif 'new' in action:
        data.stats.insert_one(stats.__dict__)
        print('\n** The new stats have been successfully added to the database! **\n')


def update_stats():
    while True:
        print('')
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date instance variable.
        user_date.date = input('Date (format YYYY-MM-DD) : ')
        # If date variable value successfully added, continue.
        if user_date.date:
            try:
                print('\nChecking database...')
                # Test the database connection.
                test_database()
                # Check if data already exists for the date.
                if user_date.validate(user_date.date, user_date.date):
                    print('\n** This date already exists in the database. **\n')
                    if user_continue('Would you like to overwrite it (y/n)? '):
                        os.system('clear')
                        print(
                            f'\nOkay, let\'s overwrite the stats for {Date.pretty_date(user_date.date)}...')
                        # Overwrite data
                        new_stats(user_date, 'overwrite')
                else:
                    print(
                        f'Please enter the new stats below : \n')
                    # Enter new data
                    new_stats(user_date, 'new')
                # Ask the user if they'd like to input more stats.
                # If no, break out of the while loop.
                if not user_continue('\nGive me more stats (y/n)? '):
                    print('Let\'s return to the menu...')
                    return
            except Exception:
                # Catch-all exception
                print('** Something\'s not right. Please try again. **')


def fetch_stats():
    while True:
        print('')
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date instance variable.
        user_date.date = input('Date (format YYYY-MM-DD) : ')
        # If date variable value successfully added, continue.
        if user_date.date:
            try:
                days_to_view = int(input('Number of days to view : '))
                user_date.range_end(days_to_view)

                try:
                    print('Checking database for data...')
                    # Test the database connection.
                    test_database()
                    # Check if data exists for the date range.
                    if user_date.validate(user_date.date, user_date.rng_end):
                        print('Fetching data...')
                        # Fetch the data from MongoDB.
                        fetched_data = aggregate_data(
                            user_date.date, user_date.rng_end)
                        # Create two lists from the data dict key and values, then merge.
                        data_lists = create_lists(fetched_data)
                        # Create a header.
                        header = f'Stats for {Date.pretty_date(user_date.date)} to {Date.pretty_date(user_date.rng_end)}'
                        # Display stats.
                        print_stats(header, data_lists)

                    # Ask the user if they'd like to view more stats.
                    # If no, break out of the while loop.
                    if not user_continue('View more stats (y/n)? '):
                        print('Let\'s return to the menu...')
                        return
                except Exception:
                    # Catch all exception
                    print('** Something\'s not right. Please try again. **')
            except ValueError:
                print(
                    '\n** Oops! Make sure to enter a number for the number of days. **')


def export_stats():
    while True:
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date obj var.
        user_date.date = input('Start date (format YYYY-MM-DD): ')
        user_date.start = user_date.date
        try:
            user_range = int(input('Number of days: '))
        except TypeError:
            print('Please enter a number.')
        user_date.end = user_date.range_end(user_range)
        simple_dates = [Date.simple_date(
            user_date.start), Date.simple_date(user_date.end)]
        # Check data exists for the above range.
        print('Checking database for data...')
        test_database()
        if user_date.validate(user_date.start, user_date.end):
            print('Fetching data...')
            data = fetch_data_range(user_date.start, user_date.end)
            data_list = list(data)
            json_file = f'stats-{simple_dates[0]}-{simple_dates[1]}.json'
            with open(json_file, 'w', encoding='utf-8') as jsonf:
                json_string = dumps(data_list, indent=4)
                jsonf.write(json_string)
            print(f'Data saved to {json_file}')
        # Ask the user if they'd like to export more stats.
        # If no, break out of the while loop.
        if not user_continue('Export more stats (y/n)? '):
            print('Let\'s return to the menu...')
            return
