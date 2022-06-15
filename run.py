import os
import time
from statbotic.welcome import welcome, stats_bot
from statbotic.authorise import login, register


def main():
    """
    * Main program function where it all begins.
    * Sets up welcome and initial menu.
    """
    while True:
        os.system('clear')
        print(welcome('Statbotic'))
        print(stats_bot())
        print('''    Hello friend! I am Statbotic!  ''')
        print('I\'m here to help you with your Support team\'s statistics.')
        print('~' * 70)
        print('\nChoose an option below : ')
        print('''
        1 : LOGIN
        2 : REGISTER
        0 : EXIT'''
              )
        choice = input('\nEnter your choice : ')

        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '0':
            print('\n>> You chose to exit - See you soon and stay awesome! :D\n')
            exit()
        print('\n** Please enter the correct number for a menu option. **')
        time.sleep(2)
        os.system('clear')


if __name__ == '__main__':
    main()
