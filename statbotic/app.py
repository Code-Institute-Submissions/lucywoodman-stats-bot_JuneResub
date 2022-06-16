import os
import time
from statbotic.welcome import welcome
from statbotic.helpers_stats import update_stats, get_stats


def app(user):
    """
    * Function for running the app.
    * Set up main menu.
    """
    while True:
        # Clear terminal to create space.
        os.system('clear')
        # Print logged-in welcome message.
        print(welcome('Statbotic'))
        print('~' * 70)
        print(f'Welcome {user.username}!')
        print('~' * 70)
        # Print the main menu.
        print('\nChoose an option below : ')
        print('''
        1 : Add or update statistics
        2 : View historic statistics
        3 : Export statistic to JSON file
        0 : EXIT'''
              )
        choice = input('\nEnter your choice : ')

        # Menu controllers.
        if choice == '1':
            update_stats()
        elif choice == '2':
            get_stats('view')
        elif choice == '3':
            get_stats('export')
        elif choice == '0':
            print('\nYou chose to exit - See you soon and stay awesome! :D\n')
            exit()
        else:
            print('\n** Please enter the correct number for a menu option. **')
            print('Returning to menu...')
        time.sleep(2)
        os.system('clear')
