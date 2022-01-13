# Local application imports
import helper
from date import Date


def capture_stats(date):
    """
    * Capture stats from the user.
    * @arg(obj) date -- the date object passed from update_stats().
    * @return(dict) statDocument -- MongoDB data structure for the stats.
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
    stats_document = {
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

    return stats_document


def update_stats(date):
    """
    * Checks the database to see if the date already exists.
    * @arg(obj) date -- the date object passed from stats_main().
    """
    exist = helper.db.stats.count_documents({"date": date}, limit=1)
    # Capture from the user.
    new_stats = capture_stats(date)
    # If the date exists in the database, updates the existing document.
    if exist:
        helper.db.stats.update_one({"date": date}, {"$set": new_stats})
        print('The stats have been successfully updated!')
    # If the date does not exist in the database, inserts a new document.
    elif not exist:
        helper.db.stats.insert_one(new_stats)
        print('The new stats have been successfully added to the database!')


def stats_input():
    """
    * Main function for inputting/updating stats in the database.
    """
    while True:
        # Run choose_date() to capture date input,
        # and return date object and string.
        print('\nWhich date would you like to input stats for?')
        date_tpl = helper.choose_date()
        date, date_str = date_tpl

        # If the date exists in the database already, offer to overwrite it.
        # If overwriting or adding new stats, run update_stats().
        if helper.db.stats.count_documents({"date": date}, limit=1):
            print('This date already exists in the database.')
            if helper.user_continue('Would you like to overwrite it (y/n)? '):
                print(
                    f'\nOkay, let\'s overwrite the stats for {date_str}.')
                update_stats(date)
        else:
            print(f'Please enter the stats for {date_str} below.')
            update_stats(date)

        # Ask the user if they'd like to input more stats.
        # If no, break out of the while loop.
        if not helper.user_continue('Give me more stats (y/n)? '):
            print('Let\'s return to the menu')
            return

def fetch_stats(*args):
    while True:
        # Create a new Date() instance.
        user_date = Date()
        # Assign input to date obj var.
        user_date.date = input('Insert a date: ')
        # Add instance variable for range start and end.
        if 'range' in args:
            user_date.start = user_date.wk_start()
            user_date.end = user_date.wk_end()
            header = f'Stats for w/c {Date.pretty_date(user_date.start)}'
        else:
            user_date.start = user_date.date
            user_date.end = user_date.date
            header = f'Stats for {Date.pretty_date(user_date.start)}'
        # Check data exists for the above range.
        print('Checking database for data...')
        user_date.validate()
        print('Fetching data...')
        data = helper.aggregate_data(user_date.start, user_date.end)
        # Another function for creating and merging lists??
        data_lists = helper.create_lists(data)
        helper.print_stats(header, data_lists)

fetch_stats()


        # # Ask the user if they'd like to view more stats.
        # # If no, break out of the while loop.
        # if not helper.user_continue('View more stats (y/n)? '):
        #     print('Let\'s return to the menu')
        #     return
