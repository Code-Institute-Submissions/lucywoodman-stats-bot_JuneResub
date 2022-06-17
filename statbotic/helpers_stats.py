import os
import time
from statbotic.title import Title
from statbotic.database import data, test_database, aggregate_data, fetch_data_range
from statbotic.helpers import user_continue, create_lists, print_stats, create_json
from statbotic.date import Date
from statbotic.stats import Stats


def new_stats(user_date, *action):
    """
    Collect new stat data to save to the database.

    * @arg(date) user_date -- passed from update_stats().
    * @arg(str) *action -- passed from update_stats().
    """
    Title('** ZenDesk Stats **').display()
    # Create a new Stats() instance
    stats = Stats()
    # Assign the previously entered date.
    stats.date = user_date.date
    # Ask for ticket comments and solves.
    stats.comments = int(input('Number of ticket responses: '))
    stats.solves = int(input('Number of ticket solves: '))
    Title('** Intercom Stats **').display()
    # Ask for chat total, wait time and CSAT score.
    stats.total = int(input('Total number of chats: '))
    stats.wait = int(input('Average chat wait time (in seconds): '))
    stats.csat = int(input('Chat CSAT score: '))
    # If overwrite is in the args, overwrite existing data.
    if 'overwrite' in action:
        data.stats.update_one({"date": user_date.date}, {
            "$set": stats.__dict__})
        print('\n** The stats have been successfully updated! **\n')
    # Else save the data as a new entry.
    elif 'new' in action:
        data.stats.insert_one(stats.__dict__)
        print('\n** The new stats have been successfully added to the database! **\n')


def update_stats():
    """
    Workflow for adding new or updating existing stats.

    * @raises(Exception) -- fallback error.
    """
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
                    # If it does exist, ask if its to be overwritten.
                    if user_continue('Would you like to overwrite it (y/n)? '):
                        os.system('clear')
                        print(
                            f'\nOkay, let\'s overwrite the stats for {Date.pretty_date(user_date.date)}...')
                        # Overwrite data
                        new_stats(user_date, 'overwrite')
                else:
                    # If it does not exist, create space and ask for new stats.
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
    """
    Fetch stats data from the database based on an input range.

    * @arg(str) *args -- passed from main menu option in app.py.
    """
    while True:
        print('')
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date instance variable.
        user_date.date = input('Start date (format YYYY-MM-DD) : ')
        # If date variable value successfully added, continue.
        if user_date.date:
            try:
                # Ask for number of days to create a date range.
                days_to_view = int(input('Extra days : '))
                user_date.range_end(days_to_view)

                try:
                    print('Checking database for data...')
                    # Test the database connection.
                    test_database()
                    # Check if data exists for the date range.
                    if user_date.validate(user_date.date, user_date.rng_end):
                        print('Fetching data...')

                        # Run the correct function depending on args.
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
                # Exception for an incorrect input.
                print(
                    '\n** Oops! Make sure to enter a number for the extra days. **')


def view_stats(user_date):
    """
    Change data to make it suitable for display using tabulate library.

    * @arg(date) user_date -- passed from get_stats().
    """
    # Fetch the data from MongoDB.
    fetched_data = aggregate_data(user_date.date, user_date.rng_end)
    # Create two lists from the data dict key and values.
    data_lists = create_lists(fetched_data)
    # Create a header.
    header = f'Stats for {Date.pretty_date(user_date.date)} to {Date.pretty_date(user_date.rng_end)}'
    # Display stats.
    print_stats(header, data_lists)


def export_stats(user_date):
    """
    Change data to prepare it to be saved to a JSON file.

    * @arg(date) user_date -- passed from get_stats().
    """
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
