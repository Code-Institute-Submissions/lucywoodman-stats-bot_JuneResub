from bson.json_util import dumps
from title import Title
from database import data, test_database, aggregate_data, fetch_data_range
from helper import user_continue, create_lists, print_stats
from date import Date
from data import Stats


def new_stats(user_date, *action):
    Title('** ZenDesk Stats **')
    stats = Stats()
    stats.date = user_date.date
    stats.comments = int(input('Number of ticket responses: '))
    stats.solves = int(input('Number of ticket solves: '))
    Title('** Intercom Stats **')
    stats.total = int(input('Total number of chats: '))
    stats.wait = int(input('Average chat wait time (in seconds): '))
    stats.csat = int(input('Chat CSAT score: '))
    if 'overwrite' in action:
        data.stats.update_one({"date": user_date.date}, {
            "$set": stats.__dict__})
        print('The stats have been successfully updated!')
    elif 'new' in action:
        data.stats.insert_one(stats.__dict__)
        print('The new stats have been successfully added to the database!')


def update_stats():
    while True:
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date obj var.
        user_date.date = input('Date (format YYYY-MM-DD): ')
        print(user_date.date)
        if user_date.date:
            try:
                # Check if data exists already for input date.
                print('\n>> Checking database...')
                test_database()
                if user_date.validate(user_date.date, user_date.date):
                    print('This date already exists in the database.')
                    if user_continue('Would you like to overwrite it (y/n)? '):
                        print(
                            f'\nOkay, let\'s overwrite the stats for {Date.pretty_date(user_date.date)}.')
                        new_stats(user_date, 'overwrite')
                else:
                    print(
                        f'Please enter the stats for {Date.pretty_date(user_date.date)} below.')
                    new_stats(user_date, 'new')
                # Ask the user if they'd like to input more stats.
                # If no, break out of the while loop.
                if not user_continue('Give me more stats (y/n)? '):
                    print('Let\'s return to the menu...')
                    return
            except:
                print('Something\'s not right. Please try again.')


def fetch_stats(*args):
    while True:
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date obj var.
        user_date.date = input('Date (format YYYY-MM-DD): ')
        # Check data exists for the above range.
        print('Checking database for data...')
        test_database()
        # Add instance variable for range start and end.
        if 'range' in args:
            user_date.start = user_date.wk_start()
            user_date.end = user_date.wk_end()
            header = f'Stats for w/c {Date.pretty_date(user_date.start)}'
        else:
            user_date.start = user_date.date
            user_date.end = user_date.date
            header = f'Stats for {Date.pretty_date(user_date.start)}'
        if user_date.validate(user_date.start, user_date.end):
            print('Fetching data...')
            data = aggregate_data(user_date.start, user_date.end)
            # Create two lists from data dict key and values, then merge.
            data_lists = create_lists(data)
            print_stats(header, data_lists)
        # Ask the user if they'd like to view more stats.
        # If no, break out of the while loop.
        if not user_continue('View more stats (y/n)? '):
            print('Let\'s return to the menu...')
            return


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
