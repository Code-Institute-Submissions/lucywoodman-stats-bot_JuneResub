# Local application imports
from helper import *


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


def stats_input():
    """
    * Main function for inputting/updating stats in the database.
    """
    while True:
        # Run choose_date() to capture date input,
        # and return date object and string.
        print('\nWhich date would you like to input stats for?')
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
        if not user_continue('input'):
            print('Let\'s return to the menu')
            return


def stats_daily():
    """
    * Asks the user to choose a date, finds the matching document in the database,
    * then displays that date's stats in a table format.
    """
    # Run choose_date() to capture date input,
    # and return date object and string.
    while True:
        print('\nWhich date would you like to view stats for?')
        date_tpl = choose_date()
        date, date_str = date_tpl

        # If the chosen date doesn't exist in the database, tell the user.
        if not db.stats.count_documents({"date": date}, limit=1):
            print(
                f'I don\'t have stats to show you for {date_str}. Choose another date.')
            continue
        else:
            # Fetch the matching document in MongoDB.
            stats_dict = db.stats.find_one({"date": date})
            # Generate the table and print.
            generate_daily_stats(date_str, stats_dict)

            # Ask the user if they'd like to view more stats.
            # If no, break out of the while loop and return to the submenu.
            if not user_continue('view'):
                print('Let\'s return to the menu')
                return


def stats_weekly():
    # Run choose_date() to capture date input,
    # and return date object and string.
    while True:
        print('\nWhich date would you like to view the weekly stats for?')
        dates_tpl = choose_week()
        wk_start, wk_end, date_str = dates_tpl

        wk_stats = stats_aggregator(wk_start, wk_end)

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

        # Ask the user if they'd like to view more stats.
        # If no, break out of the while loop.
        if not user_continue('view'):
            print('Let\'s return to the menu')
            return
