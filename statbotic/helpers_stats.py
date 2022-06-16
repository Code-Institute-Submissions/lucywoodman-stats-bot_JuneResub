import os
import time
from statbotic.title import Title
from statbotic.database import data, test_database, aggregate_data, fetch_data_range
from statbotic.helpers import user_continue, create_lists, print_stats, create_json
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
                    os.system('clear')
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


def get_stats(*args):
    while True:
        print('')
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date instance variable.
        user_date.date = input('Start date (format YYYY-MM-DD) : ')
        # If date variable value successfully added, continue.
        if user_date.date:
            try:
                print('\n(For a single day, use "0" for number of days)')
                days_to_view = int(input('Number of days : '))
                user_date.range_end(days_to_view)

                try:
                    print('Checking database for data...')
                    # Test the database connection.
                    test_database()
                    # Check if data exists for the date range.
                    if user_date.validate(user_date.date, user_date.rng_end):
                        print('Fetching data...')

                        if 'view' in args:
                            view_stats(user_date)
                        elif 'export' in args:
                            export_stats(user_date)

                    # Ask the user if they'd like to view more stats.
                    # If no, break out of the while loop.
                    if not user_continue('Continue to view stats (y/n)? '):
                        print('Let\'s return to the menu...')
                        return

                except Exception:
                    # Catch all exception
                    print('** Something\'s not right. Please try again. **')

            except ValueError:
                print(
                    '\n** Oops! Make sure to enter a number for the number of days. **')


def view_stats(user_date):
    # Fetch the data from MongoDB.
    fetched_data = aggregate_data(user_date.date, user_date.rng_end)
    # Create two lists from the data dict key and values, then merge.
    data_lists = create_lists(fetched_data)
    # Create a header.
    header = f'Stats for {Date.pretty_date(user_date.date)} to {Date.pretty_date(user_date.rng_end)}'
    # Display stats.
    print_stats(header, data_lists)


def export_stats(user_date):
    # Fetch the data from MongoDB.
    fetched_data = fetch_data_range(user_date.date, user_date.rng_end)
    # Create list from the data.
    data_list = list(fetched_data)
    # Generate simple dates for the JSON filename.
    simple_dates = [Date.simple_date(
        user_date.date), Date.simple_date(user_date.rng_end)]
    # Create JSON filename.
    json_filename = f'stats-{simple_dates[0]}-{simple_dates[1]}.json'
    # Create the JSON file
    print('Saving data to file...')
    time.sleep(2)
    create_json(data_list, json_filename)
