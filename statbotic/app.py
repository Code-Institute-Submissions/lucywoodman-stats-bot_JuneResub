import os
import time
from statbotic.welcome import welcome
from statbotic.helpers_stats import fetch_stats, update_stats, export_stats


def app():
    """
    * Function for running the statistics app.
    * Sets up logged-in menu.
    """
    while True:
        os.system('clear')
        print(welcome('Inner sanctum'))
        print('~' * 70)
        print('Welcome to hell')
        print('~' * 70)
        print('\nChoose an option below : ')
        print('''
        1 : Add or update statistics
        2 : View historic statistics
        3 : Export statistic to JSON file
        0 : EXIT'''
              )
        choice = input('\nEnter your choice : ')

        if choice == '1':
            update_stats()
        elif choice == '2':
            fetch_stats('range')
        elif choice == '3':
            export_stats()
        elif choice == '0':
            print('\nYou chose to exit - See you soon and stay awesome! :D\n')
            exit()
        print('\n** Please enter the correct number for a menu option. **')
        time.sleep(2)
        os.system('clear')
