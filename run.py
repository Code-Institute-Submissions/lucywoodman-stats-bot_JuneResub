import os
import time
from statbotic.welcome import welcome, stats_bot
from statbotic.authorise import login, register


def main():
    """
    * Main program function where it all begins.
    * Set up welcome and login menu.
    """
    while True:
        # Clear the terminal to create space.
        os.system('clear')
        # Print welcome message.
        print(welcome('Statbotic'))
        print(stats_bot())
        print('''    Hello friend! I am Statbotic!  ''')
        print('I\'m here to help you with your Support team\'s statistics.')
        print('~' * 70)
        # Print the login menu.
        print('\nChoose an option below : ')
        print('''
        1 : LOGIN
        2 : REGISTER
        0 : EXIT'''
              )
        choice = input('\nEnter your choice : ')

        # Menu controllers.
        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '0':
            print('\nYou chose to exit - See you soon and stay awesome! :D\n')
            exit()
        else:
            print('\n** Please enter the correct number for a menu option. **')
            print('Returning to menu...')
        time.sleep(2)
        os.system('clear')


if __name__ == '__main__':
    main()
