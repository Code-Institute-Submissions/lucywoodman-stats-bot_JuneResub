# Local application imports
import helper
from date import Date
from data import Stats

def new_stats(user_date, *action):
    helper.Title('** ZenDesk Stats **')
    stats = Stats()
    stats.date = user_date.date
    stats.advanced = int(input('Number of tickets advanced: '))
    stats.comments = int(input('Number of ticket public comments: '))
    stats.solved = int(input('Number of tickets solved: '))
    helper.Title('** Intercom Stats **')
    stats.total = int(input('Number of chats handled: '))
    stats.wait = int(input('Average chat wait time (in seconds): '))
    stats.csat = int(input('Chat CSAT score: '))
    if 'overwrite' in action:
        helper.db.stats.update_one({"date": user_date.date}, {"$set": stats.__dict__})
        print('The stats have been successfully updated!')
    elif 'new' in action:
        helper.db.stats.insert_one(stats.__dict__)
        print('The new stats have been successfully added to the database!')

def update_stats():
    while True:
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date obj var.
        user_date.date = input('Date (format YYYY-MM-DD): ')
        # Check if data exists already for input date.
        print('Checking database for data...')
        helper.test_database()
        if user_date.validate(user_date.date, user_date.date):
            print('This date already exists in the database.')
            if helper.user_continue('Would you like to overwrite it (y/n)? '):
                print(
                    f'\nOkay, let\'s overwrite the stats for {Date.pretty_date(user_date.date)}.')
                new_stats(user_date, 'overwrite')
        else:
            print(f'Please enter the stats for {Date.pretty_date(user_date.date)} below.')
            new_stats(user_date, 'new')
        # Ask the user if they'd like to input more stats.
        # If no, break out of the while loop.
        if not helper.user_continue('Give me more stats (y/n)? '):
            print('Let\'s return to the menu...')
            return

def fetch_stats(*args):
    while True:
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date obj var.
        user_date.date = input('Date (format YYYY-MM-DD): ')
        # Check data exists for the above range.
        print('Checking database for data...')
        helper.test_database()
        # Add instance variable for range start and end.
        if 'range' in args:
            user_date.start = user_date.wk_start()
            user_date.end = user_date.wk_end()
            user_date.validate(user_date.start, user_date.end)
            header = f'Stats for w/c {Date.pretty_date(user_date.start)}'
        else:
            user_date.validate(user_date.date, user_date.date)
            header = f'Stats for {Date.pretty_date(user_date.start)}'
        print('Fetching data...')
        data = helper.aggregate_data(user_date.start, user_date.end)
        # Another function for creating and merging lists
        data_lists = helper.create_lists(data)
        helper.print_stats(header, data_lists)
        # Ask the user if they'd like to view more stats.
        # If no, break out of the while loop.
        if not helper.user_continue('View more stats (y/n)? '):
            print('Let\'s return to the menu...')
            return
